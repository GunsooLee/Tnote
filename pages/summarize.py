import streamlit as st

def summarize_meeting():
    from transformers import pipeline

    # Hugging Face의 요약 파이프라인 생성
    summarizer = pipeline("summarization", model="gogamza/kobart-summarization", tokenizer="gogamza/kobart-summarization")

    # 요약할 텍스트
    text = """
    우리가 이제 티앱을 같이 하게 됐는데 주제를 이제 좀 정해야 될 것 같거든요. 주제를 어떤 거를 했으면 좋겠는지 좀 한번 생각해 놓은 게 있으면 조금 얘기를 해 주세요. 찬명 씨는 혹시 생각해 놓은 거 있어>요? 빅데이터도 요새 많이 하니까 좋은 것 같긴 하네요.  근데 이제 제 생각은 우리가 아직 주니어 레벨이니까그냥 언어 그러니까 시라든지 자바라든지 이런 언어도 좀 공부해 보는 것도 나쁘지 않을 것 같아요. 확실히 AI 관>련해서 기사도 많이 올라오고 그런 것 같아요.  AI 나쁘지 않은 것 같은데. 그렇죠 AI 어때요? 찬민 씨도 AI 어떻게 생각하세요?그러면 아무래도 이게 우리가 회사에서 하는 거니까 업무에 좀 적용하기 좋은 주제를 자꾸 하는 게 맞을 것 같은데요. 우리 팀에서 사용하기 좋은 업무 주제가 뭐 있을까요? AI를 만약에 한다고 하면근데 또 얘기를 들어보니까 그러면은 좀 뭔가 챗봇이라고 하면은 일단 다양한 업무에 좀 적용하기에는 좀 주제가좀 어려울 수도 있다고 좀 생각이 들어가지고 이런 거 어때요? 그냥 이렇게 뭔가 실무에서 꼭 쓰지 않더라도 다양한 업무에서 그냥 모두가 쓸 수 있는 거를 한번 생각해 보는 건 어떨지. 지금 우리 미디어 팀 말고도 다른 팀에서도 이제 다양하게 쓸 수 있는 주제를 한번 좀 생각해 보는 것도 좋을 것 같아요. 그러네요.  회의할 때 이제 저희가 회의록은 쓰니까 회의는 누구나 하기도 하고 괜찮네요. 저는 나쁘지 않은 것 같아요  그 주제.
    저는 클라우드가 좋은 것 같습니다.  요새는 클라우드에서 모든 데이터 처리하고 하는 게 많으니까클라우드 주제가 좋은 것 같습니다. 네 좋은 것 같습니다. 챗봇은 그럼 우리 팀에서만 쓸 수 있는 걸 말하는 >건가? 괜찮다. 어 그럼 회의를 요약해 주는 회의 요약 AI를 만들어 볼까요?
    요즘 또 트렌드가 빅데이터 쪽이 트렌드도 많고 저희 이제 자격증 같은 것도 이제 빅데이터 쪽 관련된 자격증이 많이 나오고 있거든요.  그래서 저희 그런 자격증 취득하면서 연구 목적으로 빅데이터 쪽 하면은 괜찮을 것 같습니다. AI를 한다 그러면 지금 아까 얘기한 것처럼 DPT도 있고 좀 분야가 많은 것 같은데 AI에서 어떤 분야가 좀 더해야 될지. 이거 조금 이거를 좀 정해야 될 것 같습니다. 제가 프로젝트 학교 다닐 때 썼던 게 이제 AI 쪽 챗봇을 한번 쓴 적이 있었거든요.  그래서 근데 그거는 이제 AI라기보다는저희가 케이스 바이 케이스를 많이 만들어가지고 이제 사용자가 입력한 그 핵심 단어만 딱 잡아가지고 그거에 관련된 거를 보여주는 챗봇>을 했던 적이 있거든요.  챗봇도 하면은 나쁘지 않을 것 같은데챗봇을 이제 지금 저희 사용자들이 물어봤을 때 이거를 답변을 해 주는 거를 하는 것도 나쁘지 않을 것 같습니다. 어쨌든 연구 목적이면은 크게 문제없지 않을까 싶은데 이건 단순하게 의견이라서 그냥 이런 것도 해봤다라고 얘기드린 거예요. 회의록 작성할 때 참고하면 괜찮은데.
    저는 좀 AI가 해보고 싶은데요.  요즘 AI가 대세잖아요.  챗gpt라든지AI 해 보면 좀 재미있을 것 같습니다. 회의 회의는 다 하는데 회의 관련된 건 어떨까요? 네 좋은 것 같아요.  회의록 요약.
    """

    # 텍스트 요약 수행 (중복 방지를 위해 no_repeat_ngram_size 파라미터 추가)
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False, no_repeat_ngram_size=3)

    return summary

st.write(summarize_meeting())
