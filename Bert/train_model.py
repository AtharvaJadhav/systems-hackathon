import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset

def train_bert_model():
    # Load data using pandas
    df = pd.read_csv('data.csv', on_bad_lines='skip')
    
    # Stratified train-validation split using pandas and sklearn
    train_df, val_df = train_test_split(df, test_size=0.1, stratify=df['label'])
    
    # Convert pandas dataframes to HuggingFace Datasets
    train_dataset = Dataset.from_pandas(train_df)
    val_dataset = Dataset.from_pandas(val_df)

    # Tokenization
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    train_dataset = train_dataset.map(lambda e: tokenizer(e['question'], truncation=True, padding='max_length', max_length=128), batched=True)
    val_dataset = val_dataset.map(lambda e: tokenizer(e['question'], truncation=True, padding='max_length', max_length=128), batched=True)
    train_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])
    val_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])

    # Define training args and train
    training_args = TrainingArguments(
        output_dir='./results',
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,  # Smaller batch size
        per_device_eval_batch_size=16,  # Smaller batch size
        num_train_epochs=3,  # Consider more epochs due to small dataset
        weight_decay=0.01,
        push_to_hub=False,
        logging_dir='./logs',
    )

    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    trainer.train()

    # Save model
    model.save_pretrained("./trained_model")
    tokenizer.save_pretrained("./trained_model")

if __name__ == "__main__":
    train_bert_model()
