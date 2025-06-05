import os
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.db import transaction
from .models import IMDGAmendment
from .tasks import split_pdf_amendment_to_pages, rename_amendment_pages_directory, delete_amendment_files_via_paths

@receiver(post_save, sender=IMDGAmendment)
def handle_amendment_save(sender, instance, created, update_fields=None, **kwargs):
    if getattr(instance, '_skip_signal_processing', False):
        return

    if kwargs.get('raw', False):
        return
    if created or not instance.pages_directory_path:
        transaction.on_commit(lambda: split_pdf_amendment_to_pages.delay(instance.id))
        return
    
    name_has_effectively_changed = False
    current_name_slug_for_dir = slugify(instance.name)
    if not current_name_slug_for_dir:
        current_name_slug_for_dir = f"amendment_{instance.id}"

    if instance.pages_directory_path:
        old_name_slug_from_path = None
        try:
            old_name_slug_from_path = os.path.basename(instance.pages_directory_path.strip(os.sep))
        except AttributeError:
            pass
        
        if old_name_slug_from_path and old_name_slug_from_path != current_name_slug_for_dir:
            name_has_effectively_changed = True
            
            transaction.on_commit(
                lambda: rename_amendment_pages_directory.delay(instance.id)
            )
    elif instance.file and not instance.pages_directory_path:
        name_has_effectively_changed = True

    needs_splitting = False
    if instance.file:
        if update_fields and 'file' in update_fields:
            needs_splitting = True
        
        elif name_has_effectively_changed:
            needs_splitting = True

        expected_current_pages_dir = os.path.join('documents', 'imdg', 'pages', current_name_slug_for_dir)
        if not instance.pages_directory_path or instance.pages_directory_path != expected_current_pages_dir:
            needs_splitting = True
        
    if needs_splitting:
        transaction.on_commit(lambda: split_pdf_amendment_to_pages.delay(instance.id))

@receiver(pre_delete, sender=IMDGAmendment)
def handle_amendment_pre_delete(sender, instance, **kwargs):
    main_file_name_to_delete = None
    if instance.file:
        main_file_name_to_delete = instance.file.name

    pages_path_to_delete = instance.pages_directory_path

    if main_file_name_to_delete or pages_path_to_delete:
        transaction.on_commit(
            lambda: delete_amendment_files_via_paths.delay(
                main_file_name_to_delete, 
                pages_path_to_delete
            )
        )