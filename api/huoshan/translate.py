import os
from fastapi import APIRouter, HTTPException, status
from config import logger
import dotenv
import json

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

from model.response import Response
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
        # 配置服务信息和 API 信息
        k_service_info = ServiceInfo(
            'translate.volcengineapi.com',
            {'Content-Type': 'application/json'},
            Credentials(HUO_SHAN_ACCESS_KEY, HUO_SHAN_SECRET_KEY, 'translate', 'cn-north-1'),
            5,
            5
        )

        k_query = {
            'Action': 'TranslateText',
            'Version': '2020-06-01'
        }
        k_api_info = {
            'translate': ApiInfo('POST', '/', k_query, {}, {})
        }

        service = Service(k_service_info, k_api_info)

        # 构造请求体
        body = {
            'TargetLanguage': request.target_language,
            'TextList': request.text,
            'SourceLanguage': request.source_language if request.source_language != "auto" else None
        }
        if body['SourceLanguage'] is None:
            del body['SourceLanguage']  # 如果 source_language 为 auto, 则移除此键

        # 调用火山翻译 API
        response = service.json('translate', {}, json.dumps(body))
        response_json = json.loads(response)

        # 记录日志
        logger.info(response_json)

        # 判断是否返回错误
        if response_json.get('ResponseMetadata', {}).get('Error') is not None:
            error = response_json['ResponseMetadata']['Error']
            logger.error(f"VolcEngine Translate API error: {error}")
            return Response.error(
                code=500,
                message=f"VolcEngine Translate API error: {error['Message']}"
            )

        # 提取翻译结果
        translated_texts = [item["Translation"] for item in response_json['TranslationList']]
        detected_language = (
            response_json['TranslationList'][0].get('DetectedSourceLanguage')
            if response_json['TranslationList']
            else None
        )

        response_data = {
            "original_texts": request.text,
            "translated_texts": translated_texts,
            "detected_source_language": detected_language
        }

        # 返回成功响应
        return Response.success(
            data=response_data
        )

    except Exception as e:
        logger.exception("Error during translation")
        # 返回错误响应
        return Response.error(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"Translation failed: {str(e)}"
        )
