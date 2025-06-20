from langchain_core.documents import Document
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from chonkie import OpenAIEmbeddings
from chonkie import SDPMChunker

from standardize import preprocess_text

import glob
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Union
import time
from pathlib import Path

load_dotenv()

api_key = os.getenv("OPENAIAPI_KEY")

DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 200

class BaseLoader:
    def __init__(self) -> None:
        pass

    def __call__(self, file_path: str, **kwargs):
        pass

class PDFLoader(BaseLoader):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, file_path: str, **kwargs):
        print(f"Đang xử lý file PDF: {file_path}")
        doc_loaded = self._load_pdf(file_path)
        print(f"Đã tải xong file PDF: {os.path.basename(file_path)}, số trang: {len(doc_loaded)}")
        return doc_loaded
    
    def _load_pdf(self, file_path):
        try:
            print(f"Đang cố gắng tải file PDF từ: {os.path.basename(file_path)}")
            pages = PyMuPDF4LLMLoader(file_path).load()
            print(f"Tải thành công {os.path.basename(file_path)} với {len(pages)} trang")
        except Exception as e:
            print(f"Lỗi khi tải file PDF {os.path.basename(file_path)}: {str(e)}")
            return []

        print(f"Đang chuyển đổi trang thành Document cho {os.path.basename(file_path)}")
        documents = [
            Document(
                page_content=preprocess_text(page.page_content),
                metadata={"page": idx + 1, "source": file_path, "filename": os.path.basename(file_path)}
            )
            for idx, page in enumerate(pages)
        ]
        print(f"Đã tạo {len(documents)} Documents cho {os.path.basename(file_path)}")
        return documents

class TextSplitter:
    def __init__(self, embedding=OpenAIEmbeddings(api_key="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",
                                            model="text-embedding-3-large")):
        self.chunker = SDPMChunker(embedding_model=embedding,  
                                   threshold=0.5,
                                   chunk_size=1024,
                                   min_sentences=2,
                                   skip_window=1)
    def __call__(self, documents):  
        all_chunks = []
        for doc in documents:
            chunks = self.chunker.chunk(doc.page_content)
            # Chuyển đổi chunks thành Document objects với metadata
            for chunk in chunks:
                all_chunks.append(Document(
                    page_content=chunk.text,
                    metadata=doc.metadata
                ))
        return all_chunks

class Loader:
    def __init__(self, supported_types: List[str] = ["pdf"]) -> None:
        print(f"Loader được khởi tạo với các loại file hỗ trợ: {supported_types}")
        self.supported_types = supported_types
        self.loaders = {
            "pdf": PDFLoader()
        }
        self.doc_splitter = TextSplitter()

    def load_single_file(self, file_path: str) -> List[Document]:
        """Load và xử lý một file đơn lẻ"""
        file_extension = Path(file_path).suffix.lower().lstrip('.')
        
        if file_extension not in self.supported_types:
            print(f"Bỏ qua file không hỗ trợ: {file_path}")
            return []
            
        if file_extension not in self.loaders:
            print(f"Không có loader cho loại file: {file_extension}")
            return []
            
        try:
            print(f"Bắt đầu xử lý file: {os.path.basename(file_path)}")
            start_time = time.time()
            
            # Load documents
            doc_loaded = self.loaders[file_extension](file_path)
            
            if not doc_loaded:
                print(f"Không thể load file: {os.path.basename(file_path)}")
                return []
            
            # Split documents
            doc_split = self.doc_splitter(doc_loaded)
            
            end_time = time.time()
            print(f"Hoàn thành xử lý {os.path.basename(file_path)} trong {end_time - start_time:.2f}s - {len(doc_split)} chunks")
            
            return doc_split
            
        except Exception as e:
            print(f"Lỗi khi xử lý file {os.path.basename(file_path)}: {str(e)}")
            return []

    def load(self, file_path: Union[str, List[str]]) -> List[Document]:
        """Load một file hoặc danh sách file"""
        if isinstance(file_path, str):
            return self.load_single_file(file_path)
        elif isinstance(file_path, list):
            return self.load_multiple_files(file_path)
        else:
            raise ValueError("file_path phải là string hoặc list của strings")

    def load_multiple_files(self, file_paths: List[str], max_workers: int = 4) -> List[Document]:
        """Load và xử lý nhiều file song song"""
        print(f"Bắt đầu xử lý {len(file_paths)} file với {max_workers} workers")
        
        all_documents = []
        completed_files = 0
        failed_files = 0
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit tất cả tasks
            future_to_file = {
                executor.submit(self.load_single_file, file_path): file_path 
                for file_path in file_paths
            }
            
            # Xử lý kết quả khi hoàn thành
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    documents = future.result()
                    if documents:
                        all_documents.extend(documents)
                        completed_files += 1
                    else:
                        failed_files += 1
                        
                    # Progress update
                    total_processed = completed_files + failed_files
                    progress = (total_processed / len(file_paths)) * 100
                    print(f"Tiến độ: {total_processed}/{len(file_paths)} ({progress:.1f}%) - "
                          f"Thành công: {completed_files}, Thất bại: {failed_files}")
                          
                except Exception as e:
                    failed_files += 1
                    print(f"Lỗi khi xử lý file {os.path.basename(file_path)}: {str(e)}")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n--- KẾT QUẢ XỬ LÝ HÀNG LOẠT ---")
        print(f"Tổng số file: {len(file_paths)}")
        print(f"Thành công: {completed_files}")
        print(f"Thất bại: {failed_files}")
        print(f"Tổng chunks: {len(all_documents)}")
        print(f"Thời gian xử lý: {total_time:.2f}s")
        print(f"Tốc độ trung bình: {len(file_paths)/total_time:.2f} file/s")
        
        return all_documents
    
    def load_dir(self, dir_path: str, max_workers: int = 4, recursive: bool = False) -> List[Document]:
        """Load tất cả file được hỗ trợ trong thư mục"""
        print(f"Đang tìm kiếm file trong thư mục: {dir_path}")
        
        all_files = []
        
        for file_type in self.supported_types:
            if recursive:
                pattern = f"{dir_path}/**/*.{file_type}"
                files = glob.glob(pattern, recursive=True)
            else:
                pattern = f"{dir_path}/*.{file_type}"
                files = glob.glob(pattern)
            
            all_files.extend(files)
            print(f"Tìm thấy {len(files)} file .{file_type}")
        
        if not all_files:
            print(f"Không tìm thấy file nào được hỗ trợ trong {dir_path}")
            return []
            
        print(f"Tổng cộng tìm thấy {len(all_files)} file")
        
        return self.load_multiple_files(all_files, max_workers)
    
    def get_file_info(self, dir_path: str, recursive: bool = False) -> dict:
        """Lấy thông tin về các file trong thư mục"""
        info = {
            "total_files": 0,
            "by_type": {},
            "file_list": []
        }
        
        for file_type in self.supported_types:
            if recursive:
                pattern = f"{dir_path}/**/*.{file_type}"
                files = glob.glob(pattern, recursive=True)
            else:
                pattern = f"{dir_path}/*.{file_type}"
                files = glob.glob(pattern)
            
            info["by_type"][file_type] = len(files)
            info["file_list"].extend(files)
            info["total_files"] += len(files)
        
        return info

if __name__ == "__main__":
    # Test với một file đơn lẻ
    loader = Loader()
    
    # Thông tin về thư mục
    data_path = "/mnt/d/Workspace/Dangerous_Good_List/langchain_chatbot/data/Part3.2_DGL.pdf"
    file_info = loader.get_file_info(data_path)
    print("=== THÔNG TIN THU MỤC ===")
    print(f"Tổng số file: {file_info['total_files']}")
    for file_type, count in file_info['by_type'].items():
        print(f"File .{file_type}: {count}")
    
    # Load tất cả file trong thư mục với 2 workers
    print("\n=== BẮT ĐẦU LOAD HÀNG LOẠT ===")
    chunks = loader.load_single_file(data_path)
    print(f"\nKẾT QUẢ CUỐI CÙNG: {len(chunks)} chunks tổng cộng")
    
    # Lưu kết quả
    output_file = "/mnt/d/Workspace/Dangerous_Good_List/langchain_chatbot/output/output_chunks_DGL.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"=== TỔNG KẾT ===\n")
        f.write(f"Số lượng chunks: {len(chunks)}\n")
        f.write(f"Các file được xử lý: {file_info['file_list']}\n\n")
        
        for i, chunk in enumerate(chunks):
            f.write(f"---- CHUNK {i+1} START ----\n")
            f.write(f"File: {chunk.metadata.get('filename', 'Unknown')}\n")
            f.write(f"Page: {chunk.metadata.get('page', 'Unknown')}\n")
            f.write(chunk.page_content + "\n")
            f.write(f"Metadata: {chunk.metadata}\n")
            f.write(f"---- CHUNK {i+1} END ----\n\n")
    
    print(f"Đã lưu kết quả vào {output_file}")