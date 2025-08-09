from DrissionPage import ChromiumPage


def automateAnswerBySQL(tab):
    index = int(tab.ele("xpath://span[@class='numb_index']").text)  # 获取题目 index
    print("========> 开始自动答题,第" + str(index) + "题")
    e_question = tab.ele("xpath://div[@class='col-xs-10 question-title']").text  # 获取答题页面题干
    e_type = tab.ele("xpath://label[@class='question-type']").text  # 获取答题页面类型
    e_A = tab.ele("xpath://div[@class='row'][2]/div[@class='col-xs-10']/div/label/div").text  # 获取答题页面选项
    e_B = tab.ele("xpath://div[@class='row'][3]/div[@class='col-xs-10']/div/label/div").text
    choice = ''
    if e_type != '[ 判断题 ]':
        print("========> 单选题 & 多选题")
        e_C = tab.ele("xpath://div[@class='row'][4]/div[@class='col-xs-10']/div/label/div").text
        e_D = tab.ele("xpath://div[@class='row'][5]/div[@class='col-xs-10']/div/label/div").text
        # choice = getAnswerBySQLSingleAndMultipleAndJudgment(e_question, e_type, e_A, e_B, e_C, e_D)
        choice = 'ABC'
    else:  # 判断题SQL
        # getAnswerBySQL(e_question,e_type,e_A)
        print("========> 判断题")
    if choice is not None:
        if len(choice) > 1:
            for part in choice.split():  # 遍历多选选项
                if part == 'A': tab.ele(
                    "xpath://div[@class='row'][2]/div[@class='col-xs-10']/div/label/span/i[1]").click()
                if part == 'B': tab.ele(
                    "xpath://div[@class='row'][3]/div[@class='col-xs-10']/div/label/span/i[1]").click()
                if part == 'C': tab.ele(
                    "xpath://div[@class='row'][4]/div[@class='col-xs-10']/div/label/span/i[1]").click()
                if part == 'D': tab.ele(
                    "xpath://div[@class='row'][5]/div[@class='col-xs-10']/div/label/span/i[1]").click()
        else:
            tab.ele("xpath://[choice]").click()  # 选择单选选项

    print("========> 自动答题,第" + str(index) + "题,答案：" + choice)

    if index < 50:
        tab.ele("xpath://next button").click()  # 下一题
        automateAnswerBySQL(tab)
    else:
        print("========> 答题完成")

if __name__ == '__main__':
    page = ChromiumPage()
    page.get("https://www.baidu.com/index.htm")
    tab = page.new_tab('')
    automateAnswerBySQL()

