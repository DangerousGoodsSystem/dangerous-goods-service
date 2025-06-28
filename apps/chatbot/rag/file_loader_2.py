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
import json
import re

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
                                   threshold=0.6,
                                   chunk_size=512,
                                   min_sentences=2,
                                   skip_window=2)
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

class MarkdownLoader(BaseLoader):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, file_path: str, **kwargs):
        print(f"Đang xử lý file Markdown: {file_path}")
        doc_loaded = self._load_markdown(file_path)
        print(f"Đã tải xong file Markdown: {os.path.basename(file_path)}, số chunks: {len(doc_loaded)}")
        return doc_loaded
    
    def _load_markdown(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self._parse_dgl_table(content, file_path)
        except Exception as e:
            print(f"Lỗi khi tải file Markdown {os.path.basename(file_path)}: {str(e)}")
            return []
    
    def _parse_dgl_table(self, content, file_path):
        """Parse bảng DGL thành chunks có cấu trúc"""
        lines = content.strip().split('\n')
        documents = []
        
        # Tìm header và separator
        header_line = None
        separator_line = None
        data_start = 0
        
        for i, line in enumerate(lines):
            if '| UN No.' in line:
                header_line = line
                if i + 1 < len(lines) and '|------' in lines[i + 1]:
                    separator_line = lines[i + 1]
                    data_start = i + 2
                break
        
        if not header_line:
            print("Không tìm thấy header của bảng DGL")
            return documents
        
        # Parse header columns
        headers = [col.strip() for col in header_line.split('|') if col.strip()]
        
        # Parse data rows
        for i in range(data_start, len(lines)):
            line = lines[i].strip()
            if not line or not line.startswith('|'):
                continue
                
            # Parse row data
            row_data = [col.strip() for col in line.split('|') if col.strip() != '']
            
            if len(row_data) < 2:  # Skip invalid rows
                continue
            
            # Tạo chunk cho mỗi hàng
            chunk_content = self._create_structured_chunk(headers, row_data, file_path)
            
            if chunk_content:
                documents.append(Document(
                    page_content=chunk_content,
                    metadata={
                        "source": file_path,
                        "filename": os.path.basename(file_path),
                        "un_number": row_data[0] if row_data else "Unknown",
                        "substance_name": row_data[1] if len(row_data) > 1 else "Unknown",
                        "type": "dangerous_goods_list"
                    }
                ))
        
        return documents
    
    def _create_structured_chunk(self, headers, row_data, file_path):
        """Tạo chunk có cấu trúc từ một hàng dữ liệu"""
        try:
            chunk_lines = [
                "DANGEROUS GOODS LIST - IMDG CODE",
                "=" * 40
            ]
            
            # Map data to headers
            for i, header in enumerate(headers[:len(row_data)]):
                if i < len(row_data) and row_data[i]:
                    chunk_lines.append(f"{header}: {row_data[i]}")
            
            chunk_lines.append("")
            chunk_lines.append(f"Source: {os.path.basename(file_path)}")
            
            return "\n".join(chunk_lines)
            
        except Exception as e:
            print(f"Lỗi khi tạo chunk: {str(e)}")
            return None

class DGLTextLoader(BaseLoader):
    def __init__(self) -> None:
        """
        Loader chuyên biệt cho file text chứa Dangerous Goods List
        với định dạng OBJECT + original_data + summarization
        """
        super().__init__()

    def __call__(self, file_path: str, **kwargs):
        print(f"Đang xử lý file DGL Text: {file_path}")
        doc_loaded = self._load_dgl_text(file_path)
        print(f"Đã tải xong file DGL Text: {os.path.basename(file_path)}, số chunks: {len(doc_loaded)}")
        return doc_loaded
    
    def _load_dgl_text(self, file_path):
        """Load file text và chia thành chunks theo object"""
        try:
            print(f"Đang đọc file: {os.path.basename(file_path)}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self._parse_dgl_objects(content, file_path)
            
        except Exception as e:
            print(f"Lỗi khi tải file DGL Text {os.path.basename(file_path)}: {str(e)}")
            return []
    
    def _parse_dgl_objects(self, content, file_path):
        """Parse các object DGL từ text"""
        documents = []
        
        # Tách theo pattern "OBJECT"
        object_pattern = r'OBJECT\s+(\d+/\d+)\s*\n'
        objects = re.split(object_pattern, content)
        
        # Bỏ qua phần đầu (trước object đầu tiên)
        if objects and not objects[0].strip().startswith('OBJECT'):
            objects = objects[1:]
        
        # Xử lý từng cặp (object_id, object_content)
        for i in range(0, len(objects), 2):
            if i + 1 < len(objects):
                object_id = objects[i].strip()
                object_content = objects[i + 1].strip()
                
                # Parse object content
                parsed_data = self._parse_single_object(object_id, object_content)
                
                if parsed_data:
                    # Tạo chunk chỉ với summarization (đơn giản)
                    chunk_content = self._create_simple_chunk(parsed_data, file_path)
                    
                    if chunk_content:
                        doc = Document(
                            page_content=chunk_content,
                            metadata={
                                "un_number": parsed_data.get("un_number"),
                                "substance_name": parsed_data.get("substance_name"),
                            }
                        )
                        documents.append(doc)
        
        print(f"Đã parse {len(documents)} objects từ file {os.path.basename(file_path)}")
        return documents
    
    def _parse_single_object(self, object_id, content):
        """Parse một object đơn lẻ"""
        try:
            lines = content.split('\n')
            
            # Tìm dòng original_data và summarization
            original_data = None
            summarization = None
            
            for line in lines:
                if line.startswith('original_data:'):
                    json_str = line.replace('original_data:', '').strip()
                    try:
                        original_data = json.loads(json_str)
                    except json.JSONDecodeError as e:
                        print(f"Lỗi parse JSON cho object {object_id}: {e}")
                        continue
                
                elif line.startswith('summarization:'):
                    summarization = line.replace('summarization:', '').strip()
            
            if summarization:
                # Trích xuất UN number từ summarization
                un_match = re.search(r'UN\s+(\d+)', summarization)
                un_number = un_match.group(1) if un_match else "Unknown"
                
                # Trích xuất tên chất từ summarization
                name_match = re.search(r'UN\s+\d+:\s*([^;]+)', summarization)
                substance_name = name_match.group(1).strip() if name_match else "Unknown"
                
                return {
                    "original_data": original_data,
                    "summarization": summarization,
                    "un_number": un_number,
                    "substance_name": substance_name
                }
            
            return None
            
        except Exception as e:
            print(f"Lỗi khi parse object {object_id}: {e}")
            return None
    
    def _create_simple_chunk(self, parsed_data, file_path):
        """Tạo chunk đơn giản chỉ với summarization"""
        try:
            # Tạo chunk content đơn giản
            chunk_lines = [
                "DANGEROUS GOODS LIST - IMDG CODE",
                "=" * 50,
                f"UN Number: {parsed_data['un_number']}",
                f"Substance: {parsed_data['substance_name']}",
                "",
                "Summary:",
                parsed_data['summarization'],
                ""
            ]
            
            return "\n".join(chunk_lines)
            
        except Exception as e:
            print(f"Lỗi khi tạo chunk: {e}")
            return None

class Loader:
    def __init__(self, supported_types: List[str] = ["pdf", "md", "txt"]) -> None:
        print(f"Loader được khởi tạo với các loại file hỗ trợ: {supported_types}")
        self.supported_types = supported_types
        self.loaders = {
            "pdf": PDFLoader(),
            "md": MarkdownLoader(),
            "txt": DGLTextLoader()  # Sử dụng DGLTextLoader cho file .txt
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
    from vector_db import VectorDB
    
    # Khởi tạo
    loader = Loader(supported_types=["txt"])
    # vector_db = VectorDB()
    
    data_path = "/mnt/d/Workspace/Dangerous_Good_List/DGL_backend_full/dangerous-goods-service/data/part1_output.txt"
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
    output_file = "/mnt/d/Workspace/Dangerous_Good_List/DGL_backend_full/dangerous-goods-service/data/chunks_part1.txt"
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
    
    # Load markdown file
    # file_path = "/mnt/d/Downloads/summaries_dgl.txt"
    # chunks = loader.load_single_file(file_path)
    
    # if chunks:        
    #     # Lưu vào vector store
    #     success = vector_db.add_data(chunks)
        
    
    #     print(f"✅ Đã lưu {len(chunks)} chunks vào vector store")
        
    #     # Test tìm kiếm chi tiết
    #     query = "what is UN 0004"
    #     print(f"\n🔍 Tìm kiếm chi tiết: '{query}'")
    #     print("=" * 80)
        
    #     retriever = vector_db.get_compressed_retriever()
    #     results = retriever.invoke(query)
        
    #     for i, chunk in enumerate(results):  
    #         print(f"\n--- CHUNK {i+1} ---")
    #         print(f"UN Number: {chunk.metadata.get('un_number')}")
    #         print(f"Substance: {chunk.metadata.get('substance_name')}")
    #         print(f"Content:\n{chunk.page_content}")
    #         print("="*60)
    # else:
    #     print("❌ Không thể đọc file txt")
    
    # query = "I need information about 2309"
    # retriever = vector_db.get_compressed_retriever()
    # results = retriever.invoke(query)
    # vector_db.pretty_print_docs_langchain(results)
        
