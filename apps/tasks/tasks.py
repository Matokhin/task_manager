import logging
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task
def task_creation_log(task_id, title, assignee):
    """
    Фоновая задача, имитирующая тяжелую операцию логирования/аудита
    при создании новой задачи пользователем.
    """
    logger.info("--------------------------------------------------")
    logger.info(f" [CELERY BACKGROUND LOG]")
    logger.info(f" СУЩНОСТЬ: Новая задача создана успешно.")
    logger.info(f" ID ЗАДАЧИ: {task_id}")
    logger.info(f" НАЗВАНИЕ: {title}")
    logger.info(f" СОЗДАТЕЛЬ: {assignee}")
    logger.info("--------------------------------------------------")
    return f"Task {task_id} logged successfully"