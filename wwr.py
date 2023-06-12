from requests import get # get은 웹사이트를 받아오는 방식
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword) :
    base_url = "https://weworkremotely.com/remote-jobs/search?term="

    response = get(f"{base_url}{keyword}")
    if response.status_code != 200 :
        print("Can not request website")
    else :
        results = []
        soup = BeautifulSoup(response.text, "html.parser") # "html.parser"는 뷰티풀수프한테 html 보낸다고 말해주는 것
        # print(response.text) # .text는 웹사이트의 모든 html  코드 받아옴
        jobs = soup.find_all('section', class_="jobs") # 클래스가 jobs인 section태그 다 찾기. 여기서 class_="jobs"는 키워드인자. 인자 위치 상관없는. 왜 키워드인자 썼냐면 find_all은 워낙 많은 인자 있어서 class_로 특정해준 것. 왜 class_로 썼냐면 class는 키워드이름이니까 if나 else를 변수명으로 못 쓰는 거랑 같은 것.
        for job_section in jobs :
            job_posts = job_section.find_all('li')
            job_posts.pop(-1) # job_posts는 리스트임. (find_all이 리스트로 반환해주나 봄.) 리스트니까 .을 찍어야지! pop()으로 몇 번째 인덱스 지울 건지 선택 가능.

            for post in job_posts :
                anchors = post.find_all('a') # anchors는 리스트 형태.
                anchor = anchors[1]
                link = anchor['href'] # beautifulsoup는 모든 html태그를 파이썬의 딕셔너리처럼 가져와줘서 이렇게 접근할 수 있는 것. anchor는 딕셔너리고 href을 가지고 있음.(hreg은 html의 속성이었지. < a href="~~~"></a> 요렇게 a태그의 속성.) 뷰티풀수프는 html태그를 가져와서 그걸 파이썬의 딕셔너리로 바꿔주는 것임!
                company, kind, region = anchor.find_all('span', class_="company") # 클래스명에 company 포함되는 클래스를 찾아주는 건 듯? 클래스명이 region company인 클래스도 가져와주는 걸 보면.
                title = anchor.find('span', class_="title") # 클래스 title인 span태그는 하나뿐인데 find_all()은 리스트 반환하니까 하나의 항목을 반환해주는 find() 써줌. find()는 그 기준에 맞는 첫 번째 항목만 반환해주는 것임!

                job_data = {
                    'link' : f"https://weworkremotely.com{link}",
                    'company' : company.string, # .string은 앞뒤 html태그코드 떼주고 태그 안의 내용 글자만 남겨줌.
                    'region' : region.string,
                    'positon' : title.string
                }
                results.append(job_data) # 리스트에 넣어줘야 for문 끝나도 사라지지 않고 계속 저장됨
        return results # 나중에 파일에 넣을 수 있게 results를 리턴시킴