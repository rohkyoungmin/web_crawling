# 크롬 드라이버 설정
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=375,812")
# options.add_argument("--headless")  # 필요 시 백그라운드 실행

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 리뷰 탭 URL 접속
base_url = "https://m.ohou.se/productions/313653/selling#production-selling-review"
driver.get(base_url)
time.sleep(3)

# 수집 변수 초기화
all_reviews = []
visited_texts = set()
visited_pages = set()
MAX_REVIEWS = 500 # <- 이 숫자만 바꾸면 원하는 숫자까지 크롤링 가능!!
page_set = 1

while len(all_reviews) < MAX_REVIEWS:
    print(f"\n[세트 {page_set}] 수집 중...")

    try:
        # paginator는 세트 단위로 바뀌므로 매번 새로 탐색
        paginator = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.production-review__paginator"))
        )

        # 페이지 세트 내 반복
        while True:
            page_buttons = paginator.find_elements(By.CSS_SELECTOR, "button._3b4ci")
            found_new_page = False

            for btn in page_buttons:
                text = btn.text.strip()
                if not text.isdigit():
                    continue

                page_num = int(text)
                if page_num in visited_pages:
                    continue

                found_new_page = True

                try:
                    # 버튼 클릭
                    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                    time.sleep(0.3)
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1)

                    # 리뷰 탭 유지
                    try:
                        review_tab = driver.find_element(By.CSS_SELECTOR, "button.production-selling__tab--review")
                        driver.execute_script("arguments[0].click();", review_tab)
                        time.sleep(1.5)
                    except:
                        print("리뷰 탭 클릭 실패 (이미 리뷰 탭일 수도 있음)")

                    # 리뷰 로딩 대기
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'production-review-item__description'))
                    )

                    print(f"페이지 {page_num} 로딩 완료")
                    visited_pages.add(page_num)

                    review_elements = driver.find_elements(By.CLASS_NAME, 'production-review-item__description')
                    score_elements = driver.find_elements(By.CLASS_NAME, 'production-review-item__writer__info__total-star')

                    count_this_page = 0
                    for review_el, score_el in zip(review_elements, score_elements):
                        review = review_el.text.strip()
                        score_text = score_el.get_attribute("aria-label")
                        score = float(score_text.replace("별점 ", "").replace("점", "")) if score_text else 5.0

                        if len(review) > 10 and review not in visited_texts:
                            all_reviews.append({
                                '페이지번호': page_num,
                                '리뷰내용': review,
                                '별점': score
                            })
                            visited_texts.add(review)
                            count_this_page += 1

                        if len(all_reviews) >= MAX_REVIEWS:
                            break

                    print(f"페이지 {page_num} 리뷰 {count_this_page}개 수집 / 누적 {len(all_reviews)}개")

                    if len(all_reviews) >= MAX_REVIEWS:
                        break

                except Exception as e:
                    print(f"페이지 {page_num} 클릭 실패: {e}")
                    continue

            if not found_new_page or len(all_reviews) >= MAX_REVIEWS:
                break

        if len(all_reviews) >= MAX_REVIEWS:
            break

        # 다음 세트로 이동
        try:
            next_button = paginator.find_element(By.CSS_SELECTOR, "button.list-paginator__next")
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)
            page_set += 1
        except:
            print("다음 세트 없음. 종료.")
            break

    except:
        print("페이지네이션 탐색 실패. 종료.")
        break

# 브라우저 종료
driver.quit()

# 감성 분석 및 CSV 저장
df = pd.DataFrame(all_reviews)
if not df.empty:
    df['리뷰번호'] = df.index + 1
    df['제품명'] = 'A가구'
    df['보관물_민감도'] = df['리뷰내용'].apply(lambda x: '민감' if any(w in x for w in ['속옷', '약', '귀중품']) else '일반')

    sentiment_dict = {
        '예쁘다': '긍정', '튼튼하다': '긍정', '만족': '긍정', '좋아요': '긍정',
        '별로': '부정', '불만': '부정', '하자': '부정', '흔들림': '부정',
        '배송': '중립', '포장': '중립'
    }

    def classify_sentiment(text):
        for word, sentiment in sentiment_dict.items():
            if word in text:
                return sentiment
        return '중립'

    def classify_emotion_type(text):
        if any(w in text for w in ['수납', '조립', '튼튼', '넉넉']):
            return '기능적'
        elif any(w in text for w in ['디자인', '예쁘다', '색상', '느낌']):
            return '심미적'
        elif any(w in text for w in ['안정감', '기분', '편안', '마음에']):
            return '정서적'
        elif any(w in text for w in ['보여', '가려', '노출', '민망']):
            return '프라이버시'
        else:
            return '기타'

    df['감성극성'] = df['리뷰내용'].apply(classify_sentiment)
    df['감성유형'] = df['리뷰내용'].apply(classify_emotion_type)

    df.to_csv("1단계_감성분석_리뷰데이터.csv", index=False, encoding='utf-8-sig')
    print(f"\n총 {len(df)}개의 리뷰가 CSV로 저장되었습니다.")
else:
    print("리뷰 데이터 없음.")

