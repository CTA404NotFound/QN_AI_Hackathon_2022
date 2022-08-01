from transformers import BertPreTrainedModel, RobertaModel, BertModel
import torch


class PhoBertAspectClassification(BertPreTrainedModel):
    """
        PhoBert Pre-trained model for aspect classification
    """

    def __init__(self, config):
        super().__init__(config)
        self.roberta = RobertaModel(config)
        self.num_classes = config.num_classes
        self.dense = torch.nn.Linear(config.hidden_size * 4, self.num_labels)

    def forward(self, input_ids, attention_mask):
        outputs = self.roberta(input_ids, attention_mask=attention_mask)
        cls_output = torch.cat((outputs[2][-1][:, 0, ...],
                                outputs[2][-2][:, 0, ...],
                                outputs[2][-3][:, 0, ...],
                                outputs[2][-4][:, 0, ...]), -1)
        features = self.dense(cls_output)
        return features
