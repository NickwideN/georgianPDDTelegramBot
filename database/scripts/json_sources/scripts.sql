SELECT ticket.id, correct_answer.number, img_source, ticket_translation.text, answer.id, answer.number, answer_translation.text, category.code, topic.description
FROM language
    LEFT JOIN ticket
    LEFT JOIN ticket_translation ON (ticket.id = ticket_translation.ticket_id AND ticket_translation.language_id=language.id)
    LEFT JOIN answer as correct_answer ON (ticket.correct_answer_id = correct_answer.id)
    LEFT JOIN answer ON (answer.ticket_id = ticket.id)
    LEFT JOIN answer_translation ON (answer_translation.answer_id = answer.id AND answer_translation.language_id = language.id)
    LEFT JOIN ticket_topic ON (ticket_topic.ticket_id = ticket.id)
    LEFT JOIN topic ON (topic.id = ticket_topic.topic_id)
    LEFT JOIN topic_translation ON (language.id = topic_translation.language_id AND topic.id = topic_translation.topic_id)
    LEFT JOIN ticket_category ON (ticket.id = ticket_category.ticket_id)
    LEFT JOIN category ON (category.id = ticket_category.category_id)
    LEFT JOIN category_translation ON (language.id = category_translation.language_id AND category.id = category_translation.category_id)
WHERE language.code = 'ru' AND ticket_category.category_id=1;

SELECT COUNT(DISTINCT ticket.id)
FROM language
    LEFT JOIN ticket
    LEFT JOIN ticket_translation ON (ticket.id = ticket_translation.ticket_id AND ticket_translation.language_id=language.id)
    LEFT JOIN answer as correct_answer ON (ticket.correct_answer_id = correct_answer.id)
    LEFT JOIN answer ON (answer.ticket_id = ticket.id)
    LEFT JOIN answer_translation ON (answer_translation.answer_id = answer.id AND answer_translation.language_id = language.id)
    LEFT JOIN ticket_topic ON (ticket_topic.ticket_id = ticket.id)
    LEFT JOIN topic ON (topic.id = ticket_topic.topic_id)
    LEFT JOIN topic_translation ON (language.id = topic_translation.language_id AND topic.id = topic_translation.topic_id)
    LEFT JOIN ticket_category ON (ticket.id = ticket_category.ticket_id)
    LEFT JOIN category ON (category.id = ticket_category.category_id)
    LEFT JOIN category_translation ON (language.id = category_translation.language_id AND category.id = category_translation.category_id)
WHERE language.code = 'ru' AND ticket_category.category_id=1;