from time import sleep

from DrissionPage import ChromiumPage
from DrissionPage._elements.none_element import NoneElement
from sqlalchemy import create_engine, Column, BigInteger, String, SmallInteger, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from datetime import datetime

Base = declarative_base()
# 创建数据库引擎
engine = create_engine('mysql://root:root@127.0.0.1:3306/spider_db', echo=True)
# 创建所有的表
Base.metadata.create_all(engine)
# 创建一个会话
Session = sessionmaker(bind=engine)
session = Session()


# 安全考试答题信息表
class SecureExampleInfo(Base):
    __tablename__ = 'a_secure_example_info'
    info_id = Column(BigInteger, primary_key=True, autoincrement=True)
    base_url = Column(String(2000), nullable=False)
    url = Column(String(2000), nullable=False)
    user_name = Column(String(200), nullable=False)
    user_email = Column(String(500), nullable=False)
    status = Column(SmallInteger, nullable=False)  # 0:未开始,1:进行中,2:完成
    create_date = Column(TIMESTAMP, nullable=False)
    update_date = Column(TIMESTAMP, nullable=False)


# 考试题库数据表
class SecureExampleDetail(Base):
    __tablename__ = 'a_secure_example_detail'
    detail_id = Column(BigInteger, primary_key=True, autoincrement=True)
    info_id = Column(BigInteger, primary_key=False)
    type = Column(String(200), nullable=False)
    tag = Column(String(200), nullable=False)
    answer = Column(String(200), nullable=False)
    question = Column(String(2000), nullable=False)
    option_A = Column(String(2000), nullable=False)
    option_B = Column(String(2000), nullable=False)
    option_C = Column(String(2000), nullable=False)
    option_D = Column(String(2000), nullable=False)
    status = Column(SmallInteger, nullable=False)  # 0:正常,1:失效
    create_date = Column(TIMESTAMP, nullable=False)
    update_date = Column(TIMESTAMP, nullable=False)


def saveInfoUrl(base_url, url, user_name, user_email):
    session.add(SecureExampleInfo(
        base_url=base_url,
        url=url,
        user_name=user_name,
        user_email=user_email,
        status=0,
        create_date=datetime.now(),
        update_date=datetime.now()
    ))
    session.commit()


def saveQuestion(details_to_insert):
    # 添加对象到会话
    session.add_all(details_to_insert)
    # 增，删，改需要提交会话 查询不需要
    session.commit()


def queryBaseInfo(info_id):
    return session.query(SecureExampleInfo).filter_by(info_id=info_id).all()[0]


def queryToDoTaskInfo():
    task_info = session.query(SecureExampleInfo).filter_by(status=0).all()
    return task_info


def updateQuestionTaskInfo(info_id, status):
    session.query(SecureExampleInfo).filter(SecureExampleInfo.info_id == info_id).update({
        "status": status,
        "update_date": datetime.now()
    })
    session.commit()


def getAnswerBySQLSingleAndMultipleAndJudgment(question, q_type, q_a, q_b, q_c, q_d):
    sql = text("""select t.formatted_answer from (
    SELECT distinct CASE
                    WHEN type = '[ 单选题 ]' THEN
                        CASE
                            WHEN answer = 'A' THEN 
                                CASE
                                 WHEN option_A LIKE concat('%', :q_a, '%') THEN 'A'
                                 WHEN option_A LIKE concat('%', :q_b, '%') THEN 'B'
                                 WHEN option_A LIKE concat('%', :q_c, '%') THEN 'C'
                                 WHEN option_A LIKE concat('%', :q_d, '%') THEN 'D'
                                 else '' end
                            WHEN answer = 'B' THEN
                                CASE
                                 WHEN option_B LIKE concat('%', :q_a, '%') THEN 'A'
                                 WHEN option_B LIKE concat('%', :q_b, '%') THEN 'B'
                                 WHEN option_B LIKE concat('%', :q_c, '%') THEN 'C'
                                 WHEN option_B LIKE concat('%', :q_d, '%') THEN 'D'
                                 else '' end
                            WHEN answer = 'C' THEN
                                CASE
                                 WHEN option_C LIKE concat('%', :q_a, '%') THEN 'A'
                                 WHEN option_C LIKE concat('%', :q_b, '%') THEN 'B'
                                 WHEN option_C LIKE concat('%', :q_c, '%') THEN 'C'
                                 WHEN option_C LIKE concat('%', :q_d, '%') THEN 'D'
                                 else '' end
                            WHEN answer = 'D' THEN
                                CASE
                                 WHEN option_D LIKE concat('%', :q_a, '%') THEN 'A'
                                 WHEN option_D LIKE concat('%', :q_b, '%') THEN 'B'
                                 WHEN option_D LIKE concat('%', :q_c, '%') THEN 'C'
                                 WHEN option_D LIKE concat('%', :q_d, '%') THEN 'D'
                                 else '' end
                            END
                    WHEN type = '[ 多选题 ]' THEN
                        CASE
                            WHEN CHAR_LENGTH(answer) = 1 THEN
                                CASE
                                    WHEN answer LIKE concat('%', 'A', '%') THEN 'A'
                                    WHEN answer LIKE concat('%', 'B', '%') THEN 'B'
                                    WHEN answer LIKE concat('%', 'C', '%') THEN 'C'
                                    WHEN answer LIKE concat('%', 'D', '%') THEN 'D'
                                    END
                            WHEN CHAR_LENGTH(answer) > 1 THEN
                                TRIM(TRAILING ', ' FROM
                                     CONCAT(
                                             IF(answer LIKE concat('%', 'A', '%'), CASE
                                                         WHEN option_A LIKE concat('%', :q_a, '%') THEN 'A'
                                                         WHEN option_A LIKE concat('%', :q_b, '%') THEN 'B'
                                                         WHEN option_A LIKE concat('%', :q_c, '%') THEN 'C'
                                                         WHEN option_A LIKE concat('%', :q_d, '%') THEN 'D'
                                                         else '' end, ''),
                                             IF(answer LIKE concat('%', 'B', '%'), CASE
                                                         WHEN option_B LIKE concat('%', :q_a, '%') THEN 'A'
                                                         WHEN option_B LIKE concat('%', :q_b, '%') THEN 'B'
                                                         WHEN option_B LIKE concat('%', :q_c, '%') THEN 'C'
                                                         WHEN option_B LIKE concat('%', :q_d, '%') THEN 'D'
                                                         else '' end, ''),
                                             IF(answer LIKE concat('%', 'C', '%'), CASE
                                                         WHEN option_C LIKE concat('%', :q_a, '%') THEN 'A'
                                                         WHEN option_C LIKE concat('%', :q_b, '%') THEN 'B'
                                                         WHEN option_C LIKE concat('%', :q_c, '%') THEN 'C'
                                                         WHEN option_C LIKE concat('%', :q_d, '%') THEN 'D'
                                                         else '' end, ''),
                                             IF(answer LIKE concat('%', 'D', '%'), CASE
                                                         WHEN option_D LIKE concat('%', :q_a, '%') THEN 'A'
                                                         WHEN option_D LIKE concat('%', :q_b, '%') THEN 'B'
                                                         WHEN option_D LIKE concat('%', :q_c, '%') THEN 'C'
                                                         WHEN option_D LIKE concat('%', :q_d, '%') THEN 'D'
                                                         else '' end, '')
                                         )
                                    )
                            END
                    WHEN type = '[ 判断题 ]' THEN
                        CASE
                            WHEN answer = 'A' THEN
                                CASE
                                     WHEN option_A LIKE concat('%', :q_a, '%') THEN 'A'
                                     WHEN option_A LIKE concat('%', :q_b, '%') THEN 'B'
                                     else '' end
                            WHEN answer = 'B' THEN
                                CASE
                                     WHEN option_B LIKE concat('%', :q_a, '%') THEN 'A'
                                     WHEN option_B LIKE concat('%', :q_b, '%') THEN 'B'
                                     else '' end
                            END
                    END AS formatted_answer
FROM a_secure_example_detail
WHERE type = :q_type
  and question = :question
) t where t.formatted_answer !='' limit 1""")
    result_row = session.execute(sql, {
        'question': question,
        'q_type': q_type,
        'q_a': q_a,
        'q_b': q_b,
        'q_c': q_c,
        'q_d': q_d
    }).fetchone()
    if result_row is not None:
        return result_row[0]
    return None


def cleanseData():
    sql_option_suffix = text("""UPDATE a_secure_example_detail
SET option_A = TRIM(BOTH '\r\n\t ' FROM REPLACE(option_A, 'A、', '')),
    option_B = TRIM(BOTH '\r\n\t ' FROM REPLACE(option_B, 'B、', '')),
    option_C = TRIM(BOTH '\r\n\t ' FROM REPLACE(option_C, 'C、', '')),
    option_D = TRIM(BOTH '\r\n\t ' FROM REPLACE(option_D, 'D、', ''))""")
    session.execute(sql_option_suffix)
    session.commit()
    sql_option_line = text("""UPDATE a_secure_example_detail SET
     option_A = REPLACE(option_A, '\n', ''),
     option_B = REPLACE(option_B, '\n', ''),
     option_C = REPLACE(option_C, '\n', ''),
     option_D = REPLACE(option_D, '\n', '')""")
    session.execute(sql_option_line)
    session.commit()

# 登录开始答题
def login(page, base_url, user_name, user_email, count):
    page.get(base_url)
    # 定位我知道了按钮
    page.ele('#btn-introduction').click()
    # 输入姓名邮箱
    page.ele('xpath://input[@placeholder="请输入姓名"]').input(user_name)
    page.ele('xpath://input[@placeholder="请输入邮箱"]').input(user_email)
    page.ele('#login').click()
    # 点击重新作答
    page.ele('xpath://div[@class="exam-end-btn"]/a[1]').click()
    # 定位我知道了按钮
    page.ele('#btn-introduction').click()
    page.ele('#toExam').click()

    if count > 0:  # 立即交卷获取题库
        saveNowInfoUrl(page, base_url, user_name, user_email)
        login(page, base_url, user_name, user_email, --count)
    elif count == 0:  # 递归立即交卷结束
        return
    else:  # 登陆后自动答题
        automateAnswerBySQL(page)
        saveNowInfoUrl(page, base_url, user_name, user_email)
        return


# 保存交卷信息
def saveNowInfoUrl(page, base_url, user_name, user_email):
    # 移动到header上点击
    sleep(0.5)  # 保存路径的问题
    page.actions.move_to('#header-partProgress').click()
    # 交卷
    page.ele('xpath://div[@class="question-panels"]/div/div[2]/button[1]').click()
    # 查看题目详情
    page.ele('xpath://div[@class="modal"]/div/div/div[@class="modal-footer"]/button[2]').click()
    sleep(0.5)  # 保存路径的问题
    # 保存题目详情信息url
    saveInfoUrl(base_url, page.url, user_name, user_email)


# 保存交卷详情页
def saveDetailUrl(page, url, info_id):
    print("========> 开始执行 info_id：" + str(info_id))
    updateQuestionTaskInfo(info_id, 1)
    # 创建页面对象，并启动或接管浏览器
    tab = page.new_tab(url)
    x = 'xpath:'
    q_xpath = '//div[@id="report-answer"]/div[@class="question" or @class="question "]'
    size = tab.eles(x + q_xpath).__len__()
    details_to_insert = []
    for index in range(1, size + 1):
        option_C = ''
        option_D = ''
        if index <= 60:  # FIXME 开始判断题
            q_c = tab.ele(x + q_xpath + '[' + str(index) + ']/ul/li[3]')
            q_d = tab.ele(x + q_xpath + '[' + str(index) + ']/ul/li[4]')
            if not isinstance(q_c, NoneElement):
                option_C = q_c.text.strip()
            if not isinstance(q_d, NoneElement):
                option_D = q_d.text.strip()
        # print(f'第{index}题')
        details_to_insert.append(
            SecureExampleDetail(
                info_id=info_id,
                type=tab.ele(x + q_xpath + '[' + str(index) + ']/div[1]/span[1]').text.strip(),
                tag=tab.ele(x + q_xpath + '[' + str(index) + ']/div[1]/span[2]').text.strip(),
                answer=tab.ele(x + q_xpath + '[' + str(index) + ']/div[4]/pre').text.strip(),
                question=tab.ele(x + q_xpath + '[' + str(index) + ']/div[2]').text.strip(),
                option_A=tab.ele(x + q_xpath + '[' + str(index) + ']/ul/li[1]').text.strip(),
                option_B=tab.ele(x + q_xpath + '[' + str(index) + ']/ul/li[2]').text.strip(),
                option_C=option_C,
                option_D=option_D,
                status=0,
                create_date=datetime.now(),
                update_date=datetime.now()))
    print("========> info_id：" + str(info_id) + " 页面解析完成开始入库，入库条数：" + str(details_to_insert.__len__()))
    saveQuestion(details_to_insert)
    print("========> info_id：" + str(info_id) + " 入库完成")
    updateQuestionTaskInfo(info_id, 2)


# 递归自动答题
def automateAnswerBySQL(tab):
    sleep(0.3)
    index = int(tab.ele("xpath://span[@class='numb_index']").text)  # 获取题目 index
    print("========> 开始自动答题,第" + str(index) + "题")
    e_question = tab.ele("xpath://div[@class='col-xs-10 question-title']").text  # 获取答题页面题干
    e_type = tab.ele("xpath://label[@class='question-type']").text  # 获取答题页面类型
    e_A = tab.ele("xpath://div[@class='row'][2]/div[@class='col-xs-10']/div/label/div").text  # 获取答题页面选项
    e_B = tab.ele("xpath://div[@class='row'][3]/div[@class='col-xs-10']/div/label/div").text
    choice = ''
    if e_type != '判断题':
        print("========> 单选题 & 多选题")
        e_C = tab.ele("xpath://div[@class='row'][4]/div[@class='col-xs-10']/div/label/div").text
        e_D = tab.ele("xpath://div[@class='row'][5]/div[@class='col-xs-10']/div/label/div").text
        choice = getAnswerBySQLSingleAndMultipleAndJudgment(e_question, '[ ' + e_type + ' ]', e_A, e_B, e_C, e_D)
    else:  # 判断题SQL
        print("========> 判断题")
        choice = getAnswerBySQLSingleAndMultipleAndJudgment(e_question, '[ ' + e_type + ' ]', e_A, e_B, '', '')
    if choice is not None:
        if len(choice) > 1:
            if choice.find('A') != -1: tab.actions.move_to(
                "xpath://div[@class='row'][2]/div[@class='col-xs-10']/div/label/span/span").click()
            if choice.find('B') != -1: tab.actions.move_to(
                "xpath://div[@class='row'][3]/div[@class='col-xs-10']/div/label/span/span").click()
            if choice.find('C') != -1: tab.actions.move_to(
                "xpath://div[@class='row'][4]/div[@class='col-xs-10']/div/label/span/span").click()
            if choice.find('D') != -1: tab.actions.move_to(
                "xpath://div[@class='row'][5]/div[@class='col-xs-10']/div/label/span/span").click()
        else:
            if choice == 'A': tab.ele(
                "xpath://div[@class='row'][2]/div[@class='col-xs-10']/div/label/span/i[1]").click()
            if choice == 'B': tab.ele(
                "xpath://div[@class='row'][3]/div[@class='col-xs-10']/div/label/span/i[1]").click()
            if choice == 'C': tab.ele(
                "xpath://div[@class='row'][4]/div[@class='col-xs-10']/div/label/span/i[1]").click()
            if choice == 'D': tab.ele(
                "xpath://div[@class='row'][5]/div[@class='col-xs-10']/div/label/span/i[1]").click()
    print("========> 自动答题,第" + str(index) + "题,答案：" + choice)
    if index < 90:  # FIXME 总题数
        tab.ele(
            "xpath://div[@class='btn-group-vertical']/button[@class='btn btn-primary exam-next-btn last']").click()  # 下一题
        automateAnswerBySQL(tab)
    else:
        print("========> 答题完成")


# 【1】获取 url 执行3次
if __name__ == '__main__1':
    baseInfo = queryBaseInfo(18)
    page = ChromiumPage()
    # 【1】获取 url 执行3次
    login(page, baseInfo.base_url, baseInfo.user_name, baseInfo.user_email, 1)

# 【2】执行已交卷的待入库题目
if __name__ == '__main__':
    page = ChromiumPage()
    secureExampleInfoList = queryToDoTaskInfo()
    for item in secureExampleInfoList:
        saveDetailUrl(page, item.url, item.info_id)
    cleanseData()


# 【3】自动登录答题
if __name__ == '__main__3':
    baseInfo = queryBaseInfo(18)  # 表中配置邮箱和姓名
    page = ChromiumPage()
    login(page, baseInfo.base_url, baseInfo.user_name, baseInfo.user_email, -1)

# 【4】自动答题（中断）
if __name__ == '__main__4':
    page = ChromiumPage()
    page.get("")
    automateAnswerBySQL(page)

# 【测试】查询题目答案
if __name__ == '__main__5':
    # 答案：
    question = "XX？"
    q_type = "[ 多选题 ]"
    q_A = ""
    q_B = ""
    q_C = ""
    q_D = ""
    result = getAnswerBySQLSingleAndMultipleAndJudgment(question, q_type, q_A, q_B, q_C, q_D)
    print(result)  # 未查到返回 None
