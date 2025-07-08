import os
from fastapi import APIRouter, HTTPException, status
from config import logger
import dotenv
import json

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

from model.translate_request import TranslateRequest

dotenv.load_dotenv()
HUO_SHAN_ACCESS_KEY = os.environ.get("HUO_SHAN_ACCESS_KEY")
HUO_SHAN_SECRET_KEY = os.environ.get("HUO_SHAN_SECRET_KEY")

router = APIRouter(
    prefix="/huoshan/translate",
    tags=["huoshan_translate"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def translate(request: TranslateRequest):
    logger.info(f"Huoshan translate endpoint called with request: {request}")

    try:
        k_service_info = ServiceInfo(
            'translate.volcengineapi.com',
            {'Content-Type': 'application/json'},
            Credentials(HUO_SHAN_ACCESS_KEY, HUO_SHAN_SECRET_KEY, 'translate', 'cn-north-1'),  # access_key, secret_key
            5,
            5)

        k_query = {
            'Action': 'TranslateText',
            'Version': '2020-06-01'
        }
        k_api_info = {
            'translate': ApiInfo('POST', '/', k_query, {}, {})
        }

        service = Service(k_service_info, k_api_info)

        # 使用 request 中的参数进行翻译
        body = {
            'TargetLanguage': request.target_language,  # 目标语言从request中获取
            'TextList': request.text,  # 待翻译文本列表从request中获取
            'SourceLanguage': request.source_language if request.source_language != "auto" else None
            # 源语言从request中获取, 并处理 auto 的情况
        }
        if body['SourceLanguage'] is None:
            del body['SourceLanguage']  # 如果 source_language 为 auto, 就不传递这个参数

        res = service.json('translate', {}, json.dumps(body))
        res_json = json.loads(res)  # 解析返回的json

        logger.info(res_json)

        if res_json.get('ResponseMetadata', {}).get('Error') is not None:  # 判断是否有错误
            error = res_json['ResponseMetadata']['Error']
            logger.error(f"VolcEngine Translate API error: {error}")
            raise HTTPException(status_code=500, detail=f"VolcEngine Translate API error: {error['Message']}")

        translated_texts = [item["Translation"] for item in res_json['TranslationList']]  # 提取翻译结果
        # 封装响应 JSON
        response_data = {
            "code": status.HTTP_200_OK,  # 使用 FastAPI 提供的 status
            "message": "Translation successful",
            "request_id": res_json.get('ResponseMetadata').get('RequestId'),  # 获取 RequestId
            "data": {
                "original_texts": request.text,
                "translated_texts": translated_texts,
                "detected_source_language": res_json['TranslationList'][0].get('DetectedSourceLanguage') if
                res_json['TranslationList'] else None  # 获取检测到的源语言(如果存在)
            }
        }
        return response_data
    except Exception as e:
        logger.exception("Error during translation")
        # 封装错误响应
        error_response = {
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Translation failed: {str(e)}",
            "request_id": None,  # 错误情况下 RequestId 可能为空
            "data": None
        }
        return error_response
