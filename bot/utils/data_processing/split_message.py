from bot.templates.messages_templates import all_table_lines_message


def split_clients_messages(clients, table_name, chunk_size=10):
    chunks = [clients[i:i + chunk_size] for i in range(0, len(clients), chunk_size)]
    
    messages = []
    for chunk in chunks:
        messages.append(all_table_lines_message(chunk, table_name)) 
    
    return messages