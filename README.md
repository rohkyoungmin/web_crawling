# 🏠 Today’s House Review Scraper & Sentiment Analyzer

This project is a Python-based web crawler and sentiment analysis tool designed to extract product reviews from the **mobile website of Today’s House (오늘의집)**. It automatically collects reviews using **Selenium automation**, performs keyword-based **sentiment polarity classification** and **emotion type categorization**, and exports the results as a CSV file.

This tool was developed as a contribution to an **LLM-driven UX research project** at a university-affiliated design lab.

---

## 📌 Key Features

* **Mobile-optimized Selenium Web Crawler**
  Automatically navigates through Today’s House mobile review pages, dynamically loads content, and scrapes up to a specified number of product reviews.

* **Duplicate Filtering & Custom Review Count Limit**
  Eliminates duplicate reviews and terminates the crawling process once the desired number of reviews is collected.

* **Automated Pagination Navigation**
  Handles page set transitions and ensures complete traversal of review pagination elements.

* **Sentiment Polarity Classification**
  Labels reviews as *Positive*, *Negative*, or *Neutral* based on keyword matching logic.

* **Emotion Type Categorization**
  Classifies user sentiment into emotional categories such as *Functional*, *Aesthetic*, *Emotional*, and *Privacy-related*.

* **CSV Export**
  Final results are saved to a `UTF-8-sig` encoded CSV file for easy downstream analysis.

---

## 💠 Technologies Used

| Technology                         | Purpose                                           |
| ---------------------------------- | ------------------------------------------------- |
| Python                             | Core scripting language                           |
| Selenium                           | Web automation and DOM interaction                |
| ChromeDriverManager                | Auto-installs compatible ChromeDriver             |
| Pandas                             | Data processing and CSV handling                  |
| WebDriverWait & ExpectedConditions | Dynamic wait conditions for asynchronous elements |
| JavaScript Execution               | For smooth interaction with mobile UI elements    |

---

## 📁 Project Structure

```
📁 Root Directory
🔹 review_scraper.py                 # Main Selenium script for crawling and sentiment labeling
🔹 requirements.txt                  # List of required Python packages
🔹 1st_stage_sentiment_reviews.csv  # Output CSV file with labeled review data
```

---

## 🧐 Sentiment Analysis Logic

### Sentiment Polarity Classification

A keyword-based dictionary determines the overall sentiment of each review:

* **Positive**: 예쁘다 (pretty), 튼튼하다 (sturdy), 만족 (satisfied), 좋아요 (good)
* **Negative**: 별로 (not great), 불만 (dissatisfied), 하자 (defect), 흔들림 (wobble)
* **Neutral**: 배송 (delivery), 포장 (packaging), or if no keyword is found

```python
sentiment_dict = {
    '예쁘다': 'Positive', '튼튼하다': 'Positive', '만족': 'Positive', '좋아요': 'Positive',
    '별로': 'Negative', '불만': 'Negative', '하자': 'Negative', '흔들림': 'Negative',
    '배송': 'Neutral', '포장': 'Neutral'
}
```

### Emotion Type Classification

User emotions are categorized based on the presence of specific functional or emotional cues:

| Type       | Keywords (in Korean)                                        |
| ---------- | ----------------------------------------------------------- |
| Functional | 수납, 조립, 튼튼, 넉넉 (storage, assembly, sturdy, spacious)        |
| Aesthetic  | 디자인, 예쁘다, 색상, 느낌 (design, appearance, color, feel)          |
| Emotional  | 안정감, 기분, 편안, 마음에 (stability, mood, comfort, satisfaction)   |
| Privacy    | 보여, 가려, 노출, 민망 (visibility, conceal, exposure, awkwardness) |
| Other      | None of the above                                           |

---

## 📈 Execution Example

```bash
$ python review_scraper.py
[Set 1] Collecting reviews...
Page 1 loaded successfully
Collected 12 reviews from Page 1 / Total: 12
...
Saved 500 reviews to CSV.
```

### Example Output (CSV)

| Review ID | Review Text       | Star Rating | Sentiment | Emotion Type | Sensitivity |
| --------- | ----------------- | ----------- | --------- | ------------ | ----------- |
| 1         | 색상이 예쁘고 수납공간이 많아요 | 5.0         | Positive  | Aesthetic    | General     |
| 2         | 약 보관용으로 샀는데 튼튼합니다 | 4.5         | Positive  | Functional   | Sensitive   |

---

## 🔧 Installation

1. Install required packages

```bash
pip install selenium pandas webdriver-manager
```

2. Ensure Chrome is installed
   The correct ChromeDriver version will be installed automatically using `webdriver-manager`.

---

## 🚀 Future Enhancements

* Integrate LLM-based sentiment classification for richer emotion detection.
* Add automated review summarization using language models.
* Deploy a web-based dashboard for real-time review monitoring.

---

## 📜 License & Ethics

This tool is intended for **educational and research purposes only**. Any use of web crawlers must comply with the [Terms of Service](https://ohou.se/terms) of Today’s House. Excessive traffic or commercial usage is strictly discouraged.

---

## 👨‍💻 Author Info

* **Developer**: Kyoungmin Roh (Cybersecurity Undergraduate | AI & Security Researcher)
* **Contribution**: Developed the web crawler for an LLM-based UX research collaboration
* **Contact**: Via GitHub issues or direct collaboration request

---

## 🌐 References

* [Today’s House Mobile](https://m.ohou.se)
* [Selenium Docs](https://www.selenium.dev/documentation/)
* [WebDriver Manager (PyPI)](https://pypi.org/project/webdriver-manager/)
