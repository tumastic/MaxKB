# -*- coding: UTF-8 -*-
"""
@Project ：MaxKB 
@File    ：deepseek_model_provider.py
@Author  ：Brian Yang
@Date    ：5/12/24 7:40 AM 
"""
import os

from common.util.file_util import get_file_content
from setting.models_provider.base_model_provider import IModelProvider, ModelProvideInfo, ModelInfo, ModelTypeConst, \
    ModelInfoManage
from setting.models_provider.impl.custom_model_provider.credential.llm import CustomLLMModelCredential
from setting.models_provider.impl.custom_model_provider.model.llm import CustomChatModel
from smartdoc.conf import PROJECT_DIR

custom_llm_model_credential = CustomLLMModelCredential()

custom_chat = ModelInfo('claude-3-5-sonnet-20240620', '自定义大模型', ModelTypeConst.LLM,
                       custom_llm_model_credential, CustomChatModel)

model_info_manage = ModelInfoManage.builder().append_model_info(custom_chat).append_default_model_info(
    custom_chat).build()

class CustomModelProvider(IModelProvider):
    def get_model_info_manage(self):
        return model_info_manage

    def get_model_provide_info(self):
        return ModelProvideInfo(provider='model_custom_provider', name='CustomLLM', icon=get_file_content(
            os.path.join(PROJECT_DIR, "apps", "setting", 'models_provider', 'impl', 'custom_model_provider', 'icon',
                         'custom_icon_svg')))