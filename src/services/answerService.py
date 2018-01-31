#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    #Author: smilesmith
    #Date: 2018-01-30
    #Desc: 答题服务
"""

# 突然发现有些逻辑放model和controller都会有较大的耦合，着手抽离：）
# model里放更纯粹的数据操作
# controller放更纯粹的区分操作（AI还是Human）
from src.models.question import Question
from src.models.answer import MyAnswer
from src.models.result import Result
from src.units import adb
from src.units.method import log_info, date_time_string
from src.daos import answerDao, questionDao

CUR_ANSWER = MyAnswer(Question('start', '0', '19700101'))


def answer_by_ai(datas, ai_type):
    """处理AI答题"""
    # 解析数据
    result = int(datas["result"])
    question_round = str(datas["question"]["questionId"])
    question_text = datas["question"]["text"]
    options = datas["options"]
    phase = date_time_string()
    if not options:
        return

    # 刷新或读取问题
    if (not isinstance(CUR_ANSWER, MyAnswer)) or CUR_ANSWER.question.round != question_round:
        question = Question(question_text, question_round, phase)
        log_info("> step 1: start [No.%s] ...", question_round)

        question_id = refresh_answer(question)
        question.set_id(question_id)
        log_info("> step 2: get question ")
    else:
        question = CUR_ANSWER.question

    # 设置选项
    CUR_ANSWER.set_option(options, ai_type)

    # 填充答案
    if ai_type == "baidu":
        results = datas["results"]
        add_result_baidu(result, options, question)
        add_result_baidu_percentage(results, question)

    elif ai_type == "sogou":
        add_result_sogou(result, options, question)

    elif ai_type == "uc":
        add_result_uc(result, options, question)

    # adb.tap_android_all(result)
    log_info("> step 3: add results: %s by %s",
             result, ai_type)


def refresh_answer(question):
    global CUR_ANSWER
    CUR_ANSWER = MyAnswer(question)
    question_id = questionDao.get_question_id(question.round, question.phase)
    print(question_id)
    if not question_id:
        question_id = questionDao.save_question(question)
    return question_id


def add_result_baidu(index, options, question):
    """添加百度AI答案"""
    prop = 0.6
    text = options[index]
    result = Result(index, text, prop, question.id)
    result.set_type("baidu")
    answerDao.save_result(result)
    CUR_ANSWER.add_result(result)


def add_result_baidu_percentage(results, question):
    """添加百度百分比答案"""
    for index, result in enumerate(results):
        result = Result(index, result['text'], result['prop'], question.id)
        result.set_type("baidu", "percentage")
        answerDao.save_result(result)
        CUR_ANSWER.add_result(result)


def add_result_sogou(index, options, question):
    """添加搜狗AI答案"""
    prop = 0.8
    text = options[index]
    result = Result(index, text, prop, question.id)
    result.set_type("sogou")
    answerDao.save_result(result)
    CUR_ANSWER.add_result(result)


def add_result_uc(index, options, question):
    """添加UC-AI答案"""
    if '、' in options[0]:
        new_results = options[0].split("、")
        for index, result_text in enumerate(new_results):
            result = Result(index, result_text, 1, question.id)
            result.set_type("uc", "single")
            answerDao.save_result(result)
            CUR_ANSWER.add_result(result)
    else:
        prop = 0.8
        text = options[index]
        result = Result(index, text, prop, question.id)
        result.set_type("uc")
        answerDao.save_result(result)
        CUR_ANSWER.add_result(result)


def answer_by_human(datas, answer_type):
    """处理人工答题"""
    result = int(datas["result"])
    question_round = str(datas["question"]["questionId"])
    adb.tap_android_all(result)
    log_info(">>> No.%s %s Answer : %s",
             question_round, answer_type, result)