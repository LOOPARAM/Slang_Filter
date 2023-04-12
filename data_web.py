#데이터 분석을 하기위한 라이브러리
import pandas as pd

#웹 크롤링을 할 수 있는 라이브러리
from bs4 import BeautifulSoup

#마찬가지로 웹 크롤링을 도와주는 라이브러리
from urllib.request import Request,urlopen

#Sleep함수를 위함
import time

#웹 크롤링하는거
import requests

#직접 버튼을 누르고 페이지에서 동작을 가능하게 해주는 라이브러리
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 크롬 드라이버 가져오기
driver = webdriver.Chrome('/usr/local/bin/chromedriver')

driver.maximize_window()

# 여러 행동을 가능하게 해주는 ActionChains를 아까 가져온 크롬 드라이버에게 적용
action = ActionChains(driver)

wait = WebDriverWait(driver, 20)

# 현재 제품의 별점 1부터 5까지 전부 크롤링하여 저장하는 함수
def OneToFive(url):

    # 매개변수로 받은 url로 접속
    driver.get(url)

    # 현재 제품의 리뷰 데이터 초기화
    data_5 = None
    data_4 = None
    data_3 = None
    data_2 = None
    data_1 = None

    # 1~5점까지의 리뷰를 반복하기 위한 for문
    for i in range(2, 7):

        # 현재 반복번째의 별점의 전체 경로 지정(항상 일관성있음)
        star_path = f'//*[@id="section_review"]/div[2]/div[2]/ul/li[{i}]/a'

        # 지정한 경로에 있는 별점버튼 가져오기
        star_btn = driver.find_element(By.XPATH, star_path)

        # 별점버튼이 있는 위치로 스크롤하기 (why? -> 가끔가다가 그냥 클릭하면 해당 위치에 다른 element가 존재해서 클릭하지 못했다는 에러가 발생함)
        action.move_to_element(star_btn).perform()

        # 로딩이 끝날때까지 잠시 대기 (이상한 값을 가져오는 경우나 에러 발생 방지)
        driver.implicitly_wait(10)

        # 별점버튼 누르기
        star_btn.click()

        # 로딩이 끝날때까지 잠시 대기 (이상한 값을 가져오는 경우나 에러 발생 방지)
        driver.implicitly_wait(10)

        # 드라이버를 통해 현재 있는 페이지의 소스를 가져와서 변수 webpage에 저장
        webpage = driver.page_source

        # 가져온 HTML를 태그로 분류하기 위해 BeautifulSoup 사용
        soup = BeautifulSoup(webpage, "html.parser")

        # 리뷰들이 총 몇개가 존재하는지 확인을 위해 리뷰 개수가 적혀있는 text의 xpath를 지정
        review_count_path = f'//*[@id="section_review"]/div[2]/div[2]/ul/li[{i}]/a/em'

        # 리뷰들의 개수가 적힌 element를 xpath에 존재하는 element로 지정
        review_count = driver.find_element(By.XPATH, review_count_path)

        # 리뷰들의 개수가 적힌 element에서 text추출해서 저장
        count_str = review_count.text

        # 추출한 text를 정수로 전환하기위해 필요없는 문자제거
        count_str = count_str.replace(',', '')
        count_str = count_str.replace('(', '')
        count_str = count_str.replace(')', '')

        # 추출한 리뷰들의 개수를 정수형태로 저장
        count = int(count_str)

        # 리뷰들의 개수를 바탕으로 몇번 반복할지 결정
        # 여기서 반복을 하는 이유는 모든 리뷰가 한페이지에서 볼 수 없기때문에 페이지를 넘겨야하는데
        # 페이지를 넘기는 버튼을 누를 횟수만큼 반복하기 위해서이다
        # 한번에 볼 수 있는 리뷰는 최대 2000개이르몰 만약 리뷰가 2000개를 넘어가면 100번 반복으로 설정
        # 아니면 리뷰들의 개수를 20으로 나눈 몫으로 지정한다 여기서 20으로 나눈 이유는 한페이지에서 볼 수 있는 리뷰가 20개이기 때문이다
        repeat = 100 if (count >= 2000) else count//20

        # 미리 지정한 반복 횟수만큼 반복하기
        for j in range(1, repeat+1):

            # 만약 반복횟수가 10미만이면
            # 여기서 이렇게 조건문을 넣은 이유는 1~10까지의 버튼의 path와 11~ 의 버튼의 path가 다르기 때문이다
            # 아래조건문들은 다 경로를 지정하므로 넘어가겠다
            if (j < 10):
                review_list_path = f'//*[@id="section_review"]/div[3]/a[{j}]'
                review_list_path_next = None
            elif (j % 10 != 0):
                review_list_path = f'//*[@id="section_review"]/div[3]/a[{j%10 + 1}]'
                review_list_path_next = None
            else:
                review_list_path = f'//*[@id="section_review"]/div[3]/a[{10 if(j == 10) else 11}]'
                review_list_path_next = f'//*[@id="section_review"]/div[3]/a[{11 if(j == 10) else 12}]'

            # 위의 조건문에서 지정한 경로에 존재하는 element를 지정
            review_list_btn = driver.find_element(By.XPATH, review_list_path)

            # # 별점버튼이 있는 위치로 스크롤하기 (why? -> 가끔가다가 그냥 클릭하면 해당 위치에 다른 element가 존재해서 클릭하지 못했다는 에러가 발생함)
            # action.move_to_element(review_list_btn).perform()

            # 로딩이 끝날때까지 잠시 대기 (이상한 값을 가져오는 경우나 에러 발생 방지)
            driver.implicitly_wait(10)

            # 넘길 리뷰페이지 버튼을 클릭하기
            review_list_btn.click()

            # 여기 if문은 너무 속도가 빨라서 미처 로딩이 안끝났는데 값을 가져오는 현상을 막기위함이다
            if (j > 1):
                # 현재 문장이라는 변수는 현재 리뷰페이지에 있는 제일 위에 리뷰를 의미한다
                now_sentence = ""

                # 전의 리뷰페이지에 있던 제일 위에 리뷰와 현재 문장이 다를때까지 반복
                while (before_sentence != now_sentence):
                    # 가져온 HTML을 class로 분류하여 댓글만 가져오기
                    webpage_just_str = str(soup.find_all(
                        attrs=('class', 'reviewItems_text__XrSSf')))

                    # 가져온 HTML에서 태그 br, em삭제
                    webpage_del_tag_str_1 = webpage_just_str.replace(
                        '<br/>', '')
                    webpage_del_tag_str_2 = webpage_del_tag_str_1.replace(
                        '<em>', '')
                    webpage_del_tag_str_3 = webpage_del_tag_str_2.replace(
                        '</em>', '')
                    webpage_del_tag_str_4 = webpage_del_tag_str_3.replace(
                        '</p>', '')

                    # 분류한 댓글들을 가각 분리하기
                    webpage_each_str = webpage_del_tag_str_4.split(
                        '<p class="reviewItems_text__XrSSf">')

                    # 첫번째 인덱스에 '[' 가 들어가서 지우기
                    webpage_each_str.remove('[')

                    # 현재 리뷰의 제일 위에 있느 리뷰를 저장
                    now_sentence = webpage_each_str[0]

            # 가져온 HTML을 class로 분류하여 댓글만 가져오기
            webpage_just_str = str(soup.find_all(
                attrs=('class', 'reviewItems_text__XrSSf')))

            # 가져온 HTML에서 태그 br, em삭제
            webpage_del_tag_str_1 = webpage_just_str.replace('<br/>', '')
            webpage_del_tag_str_2 = webpage_del_tag_str_1.replace('<em>', '')
            webpage_del_tag_str_3 = webpage_del_tag_str_2.replace('</em>', '')
            webpage_del_tag_str_4 = webpage_del_tag_str_3.replace('</p>', '')

            # 분류한 댓글들을 가각 분리하기
            webpage_each_str = webpage_del_tag_str_4.split(
                '<p class="reviewItems_text__XrSSf">')

            # 첫번째 인덱스에 '[' 가 들어가서 지우기
            webpage_each_str.remove('[')

            # 이때 변수값을 지정하면 다음 루프를 돌때 값을 사용하므로 상대적으로 이전 값이 된다
            before_sentence = webpage_each_str[0]

            # 데이터 추가
            if i == 2:
                if (data_5 == None):
                    data_5 = webpage_each_str
                else:
                    data_5 += webpage_each_str
            if i == 3:
                if (data_4 == None):
                    data_4 = webpage_each_str
                else:
                    data_4 += webpage_each_str
            if i == 4:
                if (data_3 == None):
                    data_3 = webpage_each_str
                else:
                    data_3 += webpage_each_str
            if i == 5:
                if (data_2 == None):
                    data_2 = webpage_each_str
                else:
                    data_2 += webpage_each_str
            if i == 6:
                if (data_1 == None):
                    data_1 = webpage_each_str
                else:
                    data_1 += webpage_each_str
            if (review_list_path_next != None and j != 100):
                review_list_next_btn = driver.find_element(
                    By.XPATH, review_list_path)
                # 로딩이 끝날때까지 잠시 대기 (이상한 값을 가져오는 경우나 에러 발생 방지)
                driver.implicitly_wait(10)
                review_list_next_btn.click()

    all_df_dic = {
        '5': data_5,
        '4': data_4,
        '3': data_3,
        '2': data_2,
        '1': data_1
    }

    all_df = pd.DataFrame.from_dict(all_df_dic, orient='index')

    all_df = all_df.transpose()

    return all_df
            



all_df = OneToFive("https://search.shopping.naver.com/catalog/27474323524?&NaPm=ct%3Dlfz2luow%7Cci%3D81f5d4528fbcea513e01186cb1d65507b7fc92f9%7Ctr%3Dslcc%7Csn%3D95694%7Chk%3Da082cfbec494ffee2aa29b91775900d5958cf669")
print('')


# 네이버 쇼핑 페이지 홈으로 접속하기
driver.get("https://shopping.naver.com/home")

# 카테고리 버튼 경로 지정
category_btn_path = '//*[@id="__next"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[3]/button'

# 카테고리 버튼 지정
category_btn = driver.find_element(By.XPATH, category_btn_path)

# 로딩이 끝날때까지 잠시 대기 (이상한 값을 가져오는 경우나 에러 발생 방지)
driver.implicitly_wait(10)

# 카테고리 버튼 누르기
category_btn.send_keys(Keys.ENTER)

# 카테고리 반복 횟수 찾기
category_1 = driver.find_elements(
    By.XPATH, '//*[@id="__next"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[3]/div/div/div[1]/ul/li')


# 카테고리 첫줄 반복 총 25번
for c_1 in category_1:
    c_1_a = c_1.find_element(By.TAG_NAME, 'a')
    act = action.move_to_element(c_1_a)
    act.perform()
    # 로딩이 끝날때까지 잠시 대기 (이상한 값을 가져오는 경우나 에러 발생 방지)
    driver.implicitly_wait(10)

    category_2 = driver.find_elements(
        By.XPATH, '//*[@id="__next"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[3]/div/div/div[2]/ul/li')

    for c_2 in category_2:
        c_2_a = c_2.find_element(By.TAG_NAME, 'a')
        act = action.move_to_element(c_2_a)
        act.perform()
        # 로딩이 끝날때까지 잠시 대기 (이상한 값을 가져오는 경우나 에러 발생 방지)
        driver.implicitly_wait(10)

        category_3 = driver.find_elements(
            By.XPATH, '//*[@id="__next"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[3]/div/div/div[3]/ul/li')

        for c_3 in category_3:
            c_3_a = c_3.find_element(By.TAG_NAME, 'a')
            c_3_a.send_keys(Keys.ENTER)

            # 로딩이 끝날때까지 잠시 대기 (이상한 값을 가져오는 경우나 에러 발생 방지)
            driver.implicitly_wait(10)

            many_review_btn = driver.find_element(
                By.XPATH, '//*[@id="content"]/div[1]/div[1]/div/div[1]/a[4]')

            many_review_btn.send_keys(Keys.ENTER)

            show_review = driver.find_element(
                By.XPATH, '//*[@id="content"]/div[1]/div[1]/div/div[2]/div[3]/a')

            show_review.send_keys(Keys.ENTER)

            show_review_80 = driver.find_element(
                By.XPATH, '//*[@id="content"]/div[1]/div[1]/div/div[2]/div[3]/ul/li[4]/a')

            show_review_80.send_keys(Keys.ENTER)

            time.sleep(1)

            """for element in range(1, 81):
                link = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f'//*[@id="content"]/div[1]/div[2]/div/div[{element}]/div/div/div[2]/div[1]/a'))
                )

                scroll = driver.find_element(By.XPATH, f'//*[@id="content"]/div[1]/div[2]/div/div[{element}]/div')
                

                action.scroll_to_element(scroll).perform()

                if_brand_store = WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located((
                    By.CLASS_NAME, 'basicList_brand_store__qUCFA'))
                )
                # basicList_brand_store__qUCFA
                # basicList_brand__zeEQD
                #
                print(if_brand_store.text)



                # link = WebDriverWait(driver, 10).until(
                #     EC.visibility_of_element_located(
                #         (By.XPATH, f'//*[@id="content"]/div[1]/div[2]/div/div[{element}]/div/div/div[2]/div[1]/a'))
                # )
                # scroll = WebDriverWait(driver, 10).until(
                #     EC.visibility_of_element_located(
                #         (By.XPATH, f'//*[@id="content"]/div[1]/div[2]/div/div[{element}]/div'))
                # )

                # action.scroll_to_element(scroll).perform()

                # link.send_keys(Keys.CONTROL + '\n')

                # time.sleep(5)
                # driver.implicitly_wait(100)

                # print("Current Window Handle:", driver.current_window_handle)
                # print("Current Window Title:", driver.title)

                # driver.switch_to.window(driver.window_handles[-1])

                # print("Current Window Handle:", driver.current_window_handle)
                # print("Current Window Title:", driver.title)

                # url = driver.current_url

                # if 'search.shopping.naver.com' in url:
                #     print(url)
                #     driver.close()
                #     #tabs = driver.window_handles
                # else:
                #     driver.close()

                # driver.switch_to.window(driver.window_handles[0])

                # driver.implicitly_wait(10)
            """
