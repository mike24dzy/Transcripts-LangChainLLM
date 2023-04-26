## No text file chunks output, only printouts 
# import re

# def read_transcript(file_name):
#     with open(file_name, 'r', encoding='utf-8') as file:
#         content = file.read()
#         return content

# def extract_segments(content):
#     segments = re.split(r'\n\d+\n', content)[1:]
#     return segments

# def split_into_chunks(segments, max_tokens):
#     chunks = []
#     current_chunk = []
#     current_token_count = 0

#     for segment in segments:
#         lines = segment.split('\n', 1)
#         if len(lines) == 2:
#             timestamp, text = lines
#         else:
#             timestamp, text = lines[0], ''
#         words = text.split()

#         if current_token_count + len(words) <= max_tokens:
#             current_chunk.append((timestamp, text))
#             current_token_count += len(words)
#         else:
#             chunks.append(current_chunk)
#             current_chunk = [(timestamp, text)]
#             current_token_count = len(words)

#     if current_chunk:
#         chunks.append(current_chunk)

#     return chunks

# def main():
#     file_name = 'justin_1.txt'
#     max_tokens = 2048  # Adjust this value according to your needs

#     content = read_transcript(file_name)
#     segments = extract_segments(content)
#     chunks = split_into_chunks(segments, max_tokens)

#     # for i, chunk in enumerate(chunks):
#     #     print(f'Chunk {i + 1}:')
#     #     for timestamp, text in chunk:
#     #         print(timestamp)
#     #         print(text)
#     #     print()
#     print(len(chunks))
#     print(chunks[1])

# if __name__ == '__main__':
#     main()

## Save chunks to chunks.txt file
import re

def read_transcript(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
        return content

def extract_segments(content):
    segments = re.split(r'\n\d+\n', content)[1:]
    return segments

def split_into_chunks(segments, max_tokens):
    chunks = []
    current_chunk = []
    current_token_count = 0

    for segment in segments:
        lines = segment.split('\n', 1)
        if len(lines) == 2:
            timestamp, text = lines
        else:
            timestamp, text = lines[0], ''
        words = text.split()

        if current_token_count + len(words) <= max_tokens:
            current_chunk.append((timestamp, text))
            current_token_count += len(words)
        else:
            chunks.append(current_chunk)
            current_chunk = [(timestamp, text)]
            current_token_count = len(words)

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def write_chunks_to_file(chunks, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        for i, chunk in enumerate(chunks):
            file.write(f'Chunk {i + 1}:\n')
            for timestamp, text in chunk:
                file.write(timestamp + '\n')
                file.write(text + '\n')
            file.write('\n')

def main():
    input_file_name = 'justin_1.txt'
    output_file_name = 'chunks.txt'
    max_tokens = 2048  # Adjust this value according to your needs

    content = read_transcript(input_file_name)
    segments = extract_segments(content)
    chunks = split_into_chunks(segments, max_tokens)
    write_chunks_to_file(chunks, output_file_name)
    print(f'Chunks saved to {output_file_name}')

if __name__ == '__main__':
    main()
