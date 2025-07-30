from io import BytesIO

import magic
from django.utils.translation import gettext_lazy as _

from zs_utils.data.enums import CONTENT_TYPE_TO_FILE_EXTENSION


def get_file_extension(buffer: BytesIO = None, path: str = None) -> str:
    if path:
        content_type = magic.from_file(path, mime=True)
    elif buffer:
        content_type = magic.from_buffer(buffer.read(), mime=True)
        buffer.seek(0)
    else:
        raise ValueError(_("Необходимо указать один из параметров: 'buffer' или 'path'."))

    extension = CONTENT_TYPE_TO_FILE_EXTENSION.get(content_type)
    if not extension:
        raise ValueError(
            _("Не удалось конвертировать тип файла '{content_type}' в расширение.").format(content_type=content_type)
        )
    return extension
