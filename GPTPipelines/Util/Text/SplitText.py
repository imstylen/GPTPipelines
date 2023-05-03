import tiktoken

# Define constants for the text embedding model
EMBEDDING_MODEL = 'text-embedding-ada-002'
EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = 'cl100k_base'

def split_text_by_tokens(text, token_count, split_token = ' ', remove_tokens=['\n']):
  """
  Splits a given text into smaller chunks based on the number of tokens specified.

  Args:
  text (str): The input text to be split.
  token_count (int): The maximum number of tokens allowed in each chunk.

  Returns:
  list: A list of strings where each string is a smaller chunk of the original text.
  """
  for bad_token in remove_tokens:
    # Replace new line characters with spaces
    text = text.replace(bad_token," ")

  # Get the encoding for the text embedding model
  encoding = tiktoken.get_encoding(EMBEDDING_ENCODING)

  # Encode the text using the specified encoding
  tokens = encoding.encode(text)

  # Base case: if the number of tokens is less than or equal to the token count, return the text as is
  if len(tokens) <= token_count:
    return [text]
  
  # Recursive case: split the text into two halves and recursively call the function on each half
  else:
    arr = text.split(split_token)
    mid = len(arr) // 2
    
    combine_token = split_token + ' '
    
    left = combine_token.join(arr[:mid])
    right = combine_token.join(arr[mid:])
    
    return split_text_by_tokens(left, token_count) + split_text_by_tokens(right, token_count)
