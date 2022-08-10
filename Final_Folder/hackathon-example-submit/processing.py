from tensorflow.keras.preprocessing.sequence import pad_sequences
import torch

class TextProcessing:
    def __init__(self, tokenizer: object, rdrsegmenter: object, max_length: int, shuffle: object = False) -> None:
        """
        :param sentence The review that we want to encode
        :param max_length: The maximum length of the input sequence
        :param batch_size: The number of samples to be processed in a single batch
        :param shuffle: Whether to shuffle the data or not, defaults to False (optional)
        """
        self.tokenizer = tokenizer
        self.rdrsegmenter = rdrsegmenter
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.max_length = max_length
        self.shuffle = shuffle

    def tokenizing_text(self, review: str) -> list:
        

    # def add_subword(self, sentence: str) -> list:
    #     """
    #     It takes a sentence and returns a list of subwords.

    #     :param sentence: The sentence to be tokenized
    #     :return: A list of subwords
    #     """
    #     tokenized_sentence = []
    #     for word in sentence.split():
    #         sub_words = self.tokenizer.tokenize(word)
    #         tokenized_sentence.extend(sub_words)
    #     return tokenized_sentence

    def padding_data(self, sub_words: list) -> tuple:
        """
        **The function takes in a list of subword tokens and returns a padded sequence of subword tokens and
        a list of attention masks.**

        The function uses the tokenizer to convert the subword tokens to their corresponding ids. Then it
        pads the sequence of ids to the maximum length of the sequence. The attention masks are created by
        assigning a 1 to the ids that are not 0 and a 0 to the ids that are 0

        :param sub_words: The list subwords of a sentence
        :return: x_padding and attention_masks
        """
        # print(sub_words)
        input_ids = pad_sequences([self.tokenizer.convert_tokens_to_ids(sub_words)],
                                  maxlen=self.max_length, dtype="long",
                                  value=self.tokenizer.pad_token_id,
                                  truncating="post", padding="post")
        # print(x_padding)
        input_ids_tensor = torch.tensor(input_ids).type(torch.LongTensor).to(self.device)
        input_mask = [[float(i != self.tokenizer.pad_token_id) for i in ii] for ii in input_ids]
        input_mask_tensor = torch.tensor(input_mask).type(torch.LongTensor).to(self.device)

        return input_ids_tensor, input_mask_tensor