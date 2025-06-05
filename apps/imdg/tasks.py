import os
import shutil
import fitz  # PyMuPDF
from celery import shared_task
from django.conf import settings
from django.utils.text import slugify
from django.core.files.storage import default_storage
from .models import IMDGAmendment

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def split_pdf_amendment_to_pages(self, amendment_id):
    """
    Splits an IMDGAmendment's PDF file into individual pages.
    Updates the amendment's pages_directory_path.
    Uses _skip_signal_processing flag to prevent unnecessary signal handling.
    """
    try:
        amendment = IMDGAmendment.objects.get(id=amendment_id)
    except IMDGAmendment.DoesNotExist:
        return f"IMDGAmendment with id {amendment_id} not found."

    if not amendment.file:
        return f"No file associated with IMDGAmendment id {amendment_id}."

    try:
        input_pdf_path = amendment.file.path
    except NotImplementedError:
        raise self.retry(exc=Exception("File path not accessible from storage."))
    
    slugified_name = slugify(amendment.name)
    if not slugified_name:
        slugified_name = f"amendment_{amendment.id}"

    output_dir_relative = os.path.join('documents', 'imdg', 'pages', slugified_name)
    output_directory_abs = os.path.join(settings.MEDIA_ROOT, output_dir_relative)

    doc = None
    try:
        os.makedirs(output_directory_abs, exist_ok=True)

        doc = fitz.open(input_pdf_path)
        num_pages = doc.page_count

        if num_pages == 0:
            if amendment.pages_directory_path != output_dir_relative:
                setattr(amendment, '_skip_signal_processing', True)
                try:
                    amendment.pages_directory_path = output_dir_relative
                    amendment.save(update_fields=['pages_directory_path'])
                finally:
                    if hasattr(amendment, '_skip_signal_processing'):
                        delattr(amendment, '_skip_signal_processing')
            return f"PDF for amendment '{amendment.name}' has no pages. Directory created at {output_dir_relative}."

        for i in range(num_pages):
            single_page_doc = None
            try:
                single_page_doc = fitz.open()
                single_page_doc.insert_pdf(doc, from_page=i, to_page=i)
                output_filename = os.path.join(output_directory_abs, f"{i + 1}.pdf")
                single_page_doc.save(output_filename)
            finally:
                if single_page_doc:
                    single_page_doc.close()
        
        if amendment.pages_directory_path != output_dir_relative:
            setattr(amendment, '_skip_signal_processing', True)
            try:
                amendment.pages_directory_path = output_dir_relative
                amendment.save(update_fields=['pages_directory_path'])
            finally:
                if hasattr(amendment, '_skip_signal_processing'):
                     delattr(amendment, '_skip_signal_processing')
        
        return f"Successfully split PDF for amendment '{amendment.name}' into {num_pages} pages."

    except Exception as exc:
        raise self.retry(exc=exc)
    finally:
        if doc:
            doc.close()

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def rename_amendment_pages_directory(self, amendment_id):
    """
    Renames the physical directory for an amendment's split PDF pages
    and updates the amendment's pages_directory_path in the database.
    This task assumes that when it runs, amendment.pages_directory_path
    still holds the OLD path, and amendment.name is the NEW name.
    Uses _skip_signal_processing flag for saving.
    """
    try:
        amendment = IMDGAmendment.objects.get(id=amendment_id)
    except IMDGAmendment.DoesNotExist:
        return f"IMDGAmendment with id {amendment_id} not found for renaming."

    old_output_dir_relative = amendment.pages_directory_path

    if not old_output_dir_relative:
        return f"No old path set for amendment ID {amendment_id} to rename."

    new_directory_slug = slugify(amendment.name)
    if not new_directory_slug:
        new_directory_slug = f"amendment_{amendment.id}"

    new_target_dir_relative = os.path.join('documents', 'imdg', 'pages', new_directory_slug)

    old_filesystem_dir_abs = os.path.join(settings.MEDIA_ROOT, old_output_dir_relative)
    new_filesystem_dir_abs = os.path.join(settings.MEDIA_ROOT, new_target_dir_relative)

    if old_filesystem_dir_abs == new_filesystem_dir_abs:
        if amendment.pages_directory_path != new_target_dir_relative:
            setattr(amendment, '_skip_signal_processing', True)
            try:
                amendment.pages_directory_path = new_target_dir_relative
                amendment.save(update_fields=['pages_directory_path'])
            finally:
                if hasattr(amendment, '_skip_signal_processing'):
                    delattr(amendment, '_skip_signal_processing')
        return (f"Directory path for amendment '{amendment.name}' is effectively '{new_target_dir_relative}'. "
                f"DB path ensured.")

    try:
        if os.path.exists(old_filesystem_dir_abs):
            if not os.path.exists(new_filesystem_dir_abs):
                os.rename(old_filesystem_dir_abs, new_filesystem_dir_abs)
        
        if amendment.pages_directory_path != new_target_dir_relative:
            setattr(amendment, '_skip_signal_processing', True)
            try:
                amendment.pages_directory_path = new_target_dir_relative
                amendment.save(update_fields=['pages_directory_path'])
            finally:
                if hasattr(amendment, '_skip_signal_processing'):
                    delattr(amendment, '_skip_signal_processing')
        
        return (f"Successfully processed directory path update for amendment '{amendment.name}'. "
                f"Target path is '{new_target_dir_relative}'.")

    except OSError as e:
        raise self.retry(exc=e)
    except Exception as exc:
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def delete_amendment_files_via_paths(self, main_file_name, pages_directory_path_relative):
    """
    Deletes the main PDF file and the physical directory of pages given their paths.
    Enhanced with more logging for debugging file existence.
    """
    main_file_deleted_message = f"Main file '{main_file_name}' not processed or not provided."
    if main_file_name:

        try:
            if default_storage.exists(main_file_name):
                default_storage.delete(main_file_name)
                main_file_deleted_message = f"Successfully deleted main file: {main_file_name}."
            else:
                main_file_deleted_message = f"Main file not found by default_storage.exists at path: {main_file_name}."
        except Exception as e:
            main_file_deleted_message = f"Error deleting main file {main_file_name}: {e}."

    pages_dir_deleted_message = f"Pages directory '{pages_directory_path_relative}' not processed or not provided."
    if pages_directory_path_relative:
        directory_to_delete_abs = os.path.join(settings.MEDIA_ROOT, pages_directory_path_relative)
        if os.path.exists(directory_to_delete_abs) and os.path.isdir(directory_to_delete_abs):
            try:
                shutil.rmtree(directory_to_delete_abs)
                pages_dir_deleted_message = f"Successfully deleted pages directory: {directory_to_delete_abs}."
            except OSError as e:
                
                raise self.retry(exc=e)
            except Exception as exc:
                
                raise self.retry(exc=exc)
        else:
            pages_dir_deleted_message = f"Pages directory not found or not a directory: {directory_to_delete_abs}."
    
    return f"{main_file_deleted_message} {pages_dir_deleted_message}"