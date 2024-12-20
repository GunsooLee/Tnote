import requests
import json
# import ssl
from time import sleep

#ssl._create_default_https_context = ssl._create_unverified_context

class ClovaSpeechClient:
    # Clova Speech invoke URL
    # Clova Speech secret key
    # 무료 api
    # invoke_url = 'https://clovaspeech-gw.ncloud.com/external/v1/9148/459eeca12f4c18165921361fc6f7217a4b6ce822f290d65d5bed60187a681763'
    # secret = '68c826dce2684d01bcfac8e149489997' 
    # 유료 api
    invoke_url = 'https://clovaspeech-gw.ncloud.com/external/v1/9174/5fc4aeab8b3fdd113df9f7e445550eb8f9c0b085a429272173e84df9e977b87c'
    secret = 'b71e5626a6a745e5b0c586e9c822a0ee' #유료 api
    
    res = '{"result":"SUCCEEDED","message":"Succeeded","token":"741f2bfb0e0a483fa16285d08e88ad4c","version":"ncp_v2_v2.3.2-4225de5-20240125_240319-1c1ae568_v4.2.12_ko_firedepartment_20240624_","params":{"service":"ncp","domain":"general","lang":"ko","completion":"sync","callback":"","diarization":{"enable":true,"speakerCountMin":-1,"speakerCountMax":-1},"sed":{"enable":false},"boostings":[],"forbiddens":"","wordAlignment":true,"fullText":true,"noiseFiltering":true,"priority":0,"userdata":{"_ncp_DomainCode":"emily","_ncp_DomainId":7931,"_ncp_TaskId":20762418,"_ncp_TraceId":"7ff429e399374badb552ea57ff5f9a36"}},"progress":100,"keywords":{},"segments":[{"start":1160,"end":9355,"text":"우리가 이제 티앱을 같이 하게 됐는데 주제를 이제 좀 정해야 될 것 같거든요.","confidence":0.9346,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[1750,2080,"우리가"],[2090,2300,"이제"],[3410,3800,"티앱을"],[4090,4280,"같이"],[4370,4580,"하게"],[4630,5000,"됐는데"],[6650,6980,"주제를"],[6990,7160,"이제"],[7210,7360,"좀"],[7670,8220,"정해야"],[8270,8420,"될"],[8420,8560,"것"],[8560,8940,"같거든요."]],"textEdited":"우리가 이제 티앱을 같이 하게 됐는데 주제를 이제 좀 정해야 될 것 같거든요."},{"start":9355,"end":16580,"text":"주제를 어떤 거를 했으면 좋겠는지 좀 한번 생각해 놓은 게 있으면 조금 얘기를 해 주세요.","confidence":0.9135,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[9665,9995,"주제를"],[10325,10575,"어떤"],[10765,11135,"거를"],[11165,11495,"했으면"],[11525,12095,"좋겠는지"],[12545,12695,"좀"],[13325,13495,"한번"],[13545,13915,"생각해"],[13915,14069,"놓은"],[14069,14195,"게"],[14225,14555,"있으면"],[14725,14955,"조금"],[15125,15422,"얘기를"],[15422,15555,"해"],[15555,15795,"주세요."]],"textEdited":"주제를 어떤 거를 했으면 좋겠는지 좀 한번 생각해 놓은 게 있으면 조금 얘기를 해 주세요."},{"start":17480,"end":27160,"text":"저는 클라우드가 좋은 것 같습니다. 요새는 클라우드에서 모든 데이터 처리하고 하는 게 많으니까","confidence":0.941,"diarization":{"label":"2"},"speaker":{"label":"2","name":"B","edited":false},"words":[[18090,18320,"저는"],[18470,19100,"클라우드가"],[19250,19440,"좋은"],[19490,19640,"것"],[19640,20100,"같습니다."],[20350,20980,"요새는"],[21550,22320,"클라우드에서"],[23170,23400,"모든"],[23590,23920,"데이터"],[23970,24480,"처리하고"],[25190,25400,"하는"],[25400,25520,"게"],[25530,25980,"많으니까"]],"textEdited":"저는 클라우드가 좋은 것 같습니다. 요새는 클라우드에서 모든 데이터 처리하고 하는 게 많으니까"},{"start":27160,"end":30100,"text":"클라우드 주제가 좋은 것 같습니다.","confidence":0.9807,"diarization":{"label":"2"},"speaker":{"label":"2","name":"B","edited":false},"words":[[27630,28080,"클라우드"],[28230,28560,"주제가"],[28590,28780,"좋은"],[28790,28940,"것"],[28940,29300,"같습니다."]],"textEdited":"클라우드 주제가 좋은 것 같습니다."},{"start":31000,"end":34325,"text":"찬명 씨는 혹시 생각해 놓은 거 있어요?","confidence":0.8033,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[31690,31940,"찬명"],[32030,32360,"씨는"],[32450,32700,"혹시"],[32790,33087,"생각해"],[33087,33220,"놓은"],[33220,33340,"거"],[33530,33760,"있어요?"]],"textEdited":"찬명 씨는 혹시 생각해 놓은 거 있어요?"},{"start":34325,"end":48580,"text":"요즘 또 트렌드가 빅데이터 쪽이 트렌드도 많고 저희 이제 자격증 같은 것도 이제 빅데이터 쪽 관련된 자격증이 많이 나오고 있거든요.그래서 저희 그런 자격증 취득하면서 연구 목적으로 빅데이터 쪽 하면은 괜찮을 것 같습니다.","confidence":0.9566,"diarization":{"label":"3"},"speaker":{"label":"3","name":"C","edited":false},"words":[[34835,35105,"요즘"],[35105,35225,"또"],[35355,35745,"트렌드가"],[35815,36285,"빅데이터"],[36295,36565,"쪽이"],[36755,37245,"트렌드도"],[37255,37485,"많고"],[38095,38265,"저희"],[38265,38425,"이제"],[38495,38845,"자격증"],[38855,39032,"같은"],[39032,39245,"것도"],[39245,39385,"이제"],[39395,39845,"빅데이터"],[39845,39985,"쪽"],[40075,40385,"관련된"],[40455,40832,"자격증이"],[40832,41005,"많이"],[41035,41305,"나오고"],[41315,41685,"있거든요."],[42375,42565,"그래서"],[42565,42725,"저희"],[42795,42965,"그런"],[43135,43485,"자격증"],[43535,44165,"취득하면서"],[45015,45305,"연구"],[45375,45765,"목적으로"],[45915,46345,"빅데이터"],[46395,46545,"쪽"],[46615,46965,"하면은"],[47095,47385,"괜찮을"],[47385,47492,"것"],[47492,47825,"같습니다."]],"textEdited":"요즘 또 트렌드가 빅데이터 쪽이 트렌드도 많고 저희 이제 자격증 같은 것도 이제 빅데이터 쪽 관련된 자격증이 많이 나오고 있거든요. 그래서 저희 그런 자격증 취득하면서 연구 목적으로 빅데이터 쪽 하면은 괜찮을 것 같습니다."},{"start":48610,"end":59030,"text":"빅데이터도 요새 많이 하니까 좋은 것 같긴 하네요. 근데 이제 제 생각은 우리가 아직 주니어 레벨이니까","confidence":0.9759,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[49580,50190,"빅데이터도"],[50720,50970,"요새"],[51020,51210,"많이"],[51280,51590,"하니까"],[52520,52710,"좋은"],[52720,52870,"것"],[52880,53130,"같긴"],[53160,53430,"하네요."],[54300,54490,"근데"],[54520,54710,"이제"],[55320,55470,"제"],[55500,55890,"생각은"],[56720,56990,"우리가"],[57160,57350,"아직"],[57480,57770,"주니어"],[57800,58310,"레벨이니까"]],"textEdited":"빅데이터도 요새 많이 하니까 좋은 것 같긴 하네요. 근데 이제 제 생각은 우리가 아직 주니어 레벨이니까"},{"start":59030,"end":67160,"text":"그냥 언어 그러니까 시라든지 자바라든지 이런 언어도 좀 공부해 보는 것도 나쁘지 않을 것 같아요.","confidence":0.968,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[59180,59370,"그냥"],[60340,60610,"언어"],[60820,61090,"그러니까"],[61300,61890,"시라든지"],[61920,62650,"자바라든지"],[63120,63310,"이런"],[63900,64270,"언어도"],[64340,64490,"좀"],[64580,64917,"공부해"],[64917,65137,"보는"],[65137,65370,"것도"],[65400,65770,"나쁘지"],[65770,65930,"않을"],[65960,66110,"것"],[66120,66390,"같아요."]],"textEdited":"그냥 언어 그러니까 시라든지 자바라든지 이런 언어도 좀 공부해 보는 것도 나쁘지 않을 것 같아요."},{"start":70305,"end":77595,"text":"저는 좀 AI가 해보고 싶은데요. 요즘 AI가 대세잖아요. 챗gpt라든지","confidence":0.8868,"diarization":{"label":"4"},"speaker":{"label":"4","name":"D","edited":false},"words":[[70735,71005,"저는"],[71275,71425,"좀"],[71515,72065,"AI가"],[72075,72405,"해보고"],[72405,72785,"싶은데요."],[73835,74105,"요즘"],[74235,74785,"AI가"],[74815,75485,"대세잖아요."],[75615,76745,"챗gpt라든지"]],"textEdited":"저는 좀 AI가 해보고 싶은데요. 요즘 AI가 대세잖아요. 챗gpt라든지"},{"start":77595,"end":81325,"text":"AI 해 보면 좀 재미있을 것 같습니다.","confidence":0.8435,"diarization":{"label":"4"},"speaker":{"label":"4","name":"D","edited":false},"words":[[78665,78935,"AI"],[78935,79075,"해"],[79075,79315,"보면"],[79325,79475,"좀"],[79605,79975,"재미있을"],[79975,80115,"것"],[80145,80595,"같습니다."]],"textEdited":"AI 해 보면 좀 재미있을 것 같습니다."},{"start":81325,"end":89554,"text":"확실히 AI 관련해서 기사도 많이 올라오고 그런 것 같아요. AI 나쁘지 않은 것 같은데","confidence":0.9711,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[82715,83085,"확실히"],[83755,84065,"AI"],[84255,84745,"관련해서"],[85255,85605,"기사도"],[85605,85785,"많이"],[85875,86205,"올라오고"],[86235,86405,"그런"],[86405,86512,"것"],[86512,86765,"같아요."],[87715,87965,"AI"],[88075,88405,"나쁘지"],[88405,88565,"않은"],[88575,88692,"것"],[88692,89005,"같은데"]],"textEdited":"확실히 AI 관련해서 기사도 많이 올라오고 그런 것 같아요. AI 나쁘지 않은 것 같은데"},{"start":89554,"end":91390,"text":"네 좋은 것 같습니다.","confidence":0.8946,"diarization":{"label":"2"},"speaker":{"label":"2","name":"B","edited":false},"words":[[89554,89694,"네"],[89744,89934,"좋은"],[89944,90061,"것"],[90061,90454,"같습니다."]],"textEdited":"네 좋은 것 같습니다."},{"start":91480,"end":95565,"text":"그렇죠 AI 어때요? 찬민 씨도 AI 어떻게 생각하세요?","confidence":0.7906,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[92090,92320,"그렇죠"],[92610,92880,"AI"],[93170,93400,"어때요?"],[93490,93700,"찬민"],[93710,93920,"씨도"],[93970,94200,"AI"],[94650,94860,"어떻게"],[94930,95380,"생각하세요?"]],"textEdited":"그렇죠 AI 어때요? 찬민 씨도 AI 어떻게 생각하세요?"},{"start":95565,"end":104675,"text":"AI를 한다 그러면 지금 아까 얘기한 것처럼 DPT도 있고 좀 분야가 많은 것 같은데 AI에서 어떤 분야가 좀 더","confidence":0.9461,"diarization":{"label":"3"},"speaker":{"label":"3","name":"C","edited":false},"words":[[95895,96505,"AI를"],[96505,96705,"한다"],[96735,97025,"그러면"],[97455,97645,"지금"],[97675,97865,"아까"],[97895,98165,"얘기한"],[98165,98425,"것처럼"],[99095,99545,"DPT도"],[99545,99705,"있고"],[100555,100705,"좀"],[100855,101165,"분야가"],[101195,101425,"많은"],[101435,101585,"것"],[101585,101905,"같은데"],[102435,102925,"AI에서"],[102935,103145,"어떤"],[103195,103485,"분야가"],[103615,103765,"좀"],[103775,103925,"더"]],"textEdited":"AI를 한다 그러면 지금 아까 얘기한 것처럼 DPT도 있고 좀 분야가 많은 것 같은데 AI에서 어떤 분야가 좀 더"},{"start":104675,"end":107760,"text":"해야 될지 이거 조금 이거를 좀 정해야 될 것 같습니다.","confidence":0.9574,"diarization":{"label":"3"},"speaker":{"label":"3","name":"C","edited":false},"words":[[105205,105435,"해야"],[105435,105755,"될지"],[105825,106015,"이거"],[106025,106235,"조금"],[106345,106635,"이거를"],[106645,106795,"좀"],[106795,107009,"정해야"],[107009,107102,"될"],[107102,107189,"것"],[107189,107475,"같습니다."]],"textEdited":"해야 될지 이거 조금 이거를 좀 정해야 될 것 같습니다."},{"start":107760,"end":118305,"text":"그러면 아무래도 이게 우리가 회사에서 하는 거니까 업무에 좀 적용하기 좋은 주제를 자꾸 하는 게 맞을 것 같은데요.","confidence":0.9909,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[109290,109640,"그러면"],[109650,110080,"아무래도"],[110390,110560,"이게"],[111150,111420,"우리가"],[112090,112540,"회사에서"],[112540,112740,"하는"],[112740,113040,"거니까"],[113570,113960,"업무에"],[113990,114140,"좀"],[114310,114840,"적용하기"],[115030,115200,"좋은"],[115430,115780,"주제를"],[115850,116040,"자꾸"],[116130,116380,"하는"],[116390,116540,"게"],[116810,117040,"맞을"],[117050,117200,"것"],[117210,117600,"같은데요."]],"textEdited":"그러면 아무래도 이게 우리가 회사에서 하는 거니까 업무에 좀 적용하기 좋은 주제를 자꾸 하는 게 맞을 것 같은데요."},{"start":118305,"end":124740,"text":"우리 팀에서 사용하기 좋은 업무 주제가 뭐 있을까요? AI를 만약에 한다고 하면","confidence":0.9555,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[118655,118865,"우리"],[118875,119265,"팀에서"],[120055,120445,"사용하기"],[120445,120605,"좋은"],[120695,120885,"업무"],[120995,121465,"주제가"],[121635,121785,"뭐"],[122175,122585,"있을까요?"],[122735,123165,"AI를"],[123165,123445,"만약에"],[123445,123725,"한다고"],[123725,123925,"하면"]],"textEdited":"우리 팀에서 사용하기 좋은 업무 주제가 뭐 있을까요? AI를 만약에 한다고 하면"},{"start":127260,"end":137225,"text":"제가 프로젝트 학교 다닐 때 썼던 게 이제 AI 쪽 챗봇을 한번 쓴 적이 있었거든요. 그래서 근데 그거는 이제 AI라기보다는","confidence":0.9867,"diarization":{"label":"3"},"speaker":{"label":"3","name":"C","edited":false},"words":[[128130,128340,"제가"],[128470,128900,"프로젝트"],[129090,129360,"학교"],[129360,129560,"다닐"],[129560,129700,"때"],[129750,130020,"썼던"],[130070,130220,"게"],[130330,130500,"이제"],[130590,130840,"AI"],[130930,131080,"쪽"],[131210,132300,"챗봇을"],[132300,132500,"한번"],[132570,132720,"쓴"],[132720,132960,"적이"],[132960,133400,"있었거든요."],[134150,134340,"그래서"],[135070,135260,"근데"],[135350,135587,"그거는"],[135587,135740,"이제"],[135810,136720,"AI라기보다는"]],"textEdited":"제가 프로젝트 학교 다닐 때 썼던 게 이제 AI 쪽 챗봇을 한번 쓴 적이 있었거든요. 그래서 근데 그거는 이제 AI라기보다는"},{"start":137225,"end":140195,"text":"저희가 케이스 바이 케이스를 많이 만들어가지고","confidence":0.9208,"diarization":{"label":"3"},"speaker":{"label":"3","name":"C","edited":false},"words":[[137475,137725,"저희가"],[137795,138165,"케이스"],[138165,138385,"바이"],[138385,138732,"케이스를"],[138732,138885,"많이"],[138955,139585,"만들어가지고"]],"textEdited":"저희가 케이스 바이 케이스를 많이 만들어가지고"},{"start":140195,"end":151204,"text":"이제 사용자가 입력한 그 핵심 단어만 딱 잡아가지고 그거에 관련된 거를 보여주는 챗봇을 했던 적이 있거든요. 챗봇도 하면은 나쁘지 않을 것 같은데","confidence":0.9567,"diarization":{"label":"3"},"speaker":{"label":"3","name":"C","edited":false},"words":[[140405,140575,"이제"],[140685,141175,"사용자가"],[141185,141535,"입력한"],[141785,141935,"그"],[141945,142235,"핵심"],[142425,142755,"단어만"],[142885,143035,"딱"],[143265,143775,"잡아가지고"],[143825,144122,"그거에"],[144122,144475,"관련된"],[144565,144815,"거를"],[145205,145595,"보여주는"],[145865,146235,"챗봇을"],[146625,146855,"했던"],[146855,147075,"적이"],[147075,147355,"있거든요."],[148025,148395,"챗봇도"],[148765,149135,"하면은"],[149165,149442,"나쁘지"],[149442,149562,"않을"],[149562,149695,"것"],[150285,150615,"같은데"]],"textEdited":"이제 사용자가 입력한 그 핵심 단어만 딱 잡아가지고 그거에 관련된 거를 보여주는 챗봇을 했던 적이 있거든요. 챗봇도 하면은 나쁘지 않을 것 같은데"},{"start":151204,"end":161290,"text":"챗봇을 이제 지금 저희 사용자들이 물어봤을 때 이거를 답변을 해 주는 거를 하는 것도 나쁘지 않을 것 같습니다.","confidence":0.9759,"diarization":{"label":"3"},"speaker":{"label":"3","name":"C","edited":false},"words":[[151414,151804,"챗봇을"],[151804,151964,"이제"],[153234,153424,"지금"],[153424,153584,"저희"],[153614,155104,"사용자들이"],[156334,156731,"물어봤을"],[156731,156864,"때"],[156864,157124,"이거를"],[157174,157504,"답변을"],[157754,157904,"해"],[157904,158164,"주는"],[158164,158404,"거를"],[158874,159104,"하는"],[159104,159304,"것도"],[159304,159551,"나쁘지"],[159551,159704,"않을"],[159704,159791,"것"],[159791,160104,"같습니다."]],"textEdited":"챗봇을 이제 지금 저희 사용자들이 물어봤을 때 이거를 답변을 해 주는 거를 하는 것도 나쁘지 않을 것 같습니다."},{"start":168610,"end":177870,"text":"챗봇은 그럼 우리 팀에서만 쓸 수 있는 걸 말하는 건가?","confidence":0.9604,"diarization":{"label":"2"},"speaker":{"label":"2","name":"B","edited":false},"words":[[171760,172310,"챗봇은"],[173300,173490,"그럼"],[173980,174190,"우리"],[174320,175230,"팀에서만"],[175440,175590,"쓸"],[175620,175770,"수"],[175800,175990,"있는"],[176140,176290,"걸"],[176400,176750,"말하는"],[176750,177050,"건가?"]],"textEdited":"챗봇은 그럼 우리 팀에서만 쓸 수 있는 걸 말하는 건가?"},{"start":178450,"end":184030,"text":"어쨌든 연구 목적이면은 크게 문제없지 않을까 싶은데","confidence":0.9336,"diarization":{"label":"3"},"speaker":{"label":"3","name":"C","edited":false},"words":[[179060,179330,"어쨌든"],[179380,179650,"연구"],[179720,180330,"목적이면은"],[181180,181390,"크게"],[181440,181850,"문제없지"],[181880,182230,"않을까"],[182420,182770,"싶은데"]],"textEdited":"어쨌든 연구 목적이면은 크게 문제없지 않을까 싶은데"},{"start":184680,"end":190290,"text":"이건 단순하게 의견이라서 그냥 이런 것도 해봤다라고 얘기드린 거예요.","confidence":0.9738,"diarization":{"label":"3"},"speaker":{"label":"3","name":"C","edited":false},"words":[[185470,185640,"이건"],[185670,186080,"단순하게"],[186110,186680,"의견이라서"],[187310,187480,"그냥"],[187910,188100,"이런"],[188100,188247,"것도"],[188247,189340,"해봤다라고"],[189340,189680,"얘기드린"],[189680,189900,"거예요."]],"textEdited":"이건 단순하게 의견이라서 그냥 이런 것도 해봤다라고 얘기드린 거예요."},{"start":190290,"end":200275,"text":"근데 또 얘기를 들어보니까 그러면은 좀 뭔가 챗봇이라고 하면은 일단 다양한 업무에 좀 적용하기에는 좀 주제가","confidence":0.9675,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[190560,190770,"근데"],[190770,190910,"또"],[190940,191250,"얘기를"],[191260,191830,"들어보니까"],[192860,193350,"그러면은"],[193580,193730,"좀"],[193800,194010,"뭔가"],[194200,194757,"챗봇이라고"],[194757,195130,"하면은"],[195640,195810,"일단"],[196340,196690,"다양한"],[196780,197090,"업무에"],[197100,197250,"좀"],[197560,198510,"적용하기에는"],[199020,199170,"좀"],[199300,199650,"주제가"]],"textEdited":"근데 또 얘기를 들어보니까 그러면은 좀 뭔가 챗봇이라고 하면은 일단 다양한 업무에 좀 적용하기에는 좀 주제가"},{"start":200275,"end":207430,"text":"좀 어려울 수도 있다고 좀 생각이 들어가지고 이런 거 어때요? 그냥 이렇게 뭔가","confidence":0.973,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[200425,200575,"좀"],[200575,200875,"어려울"],[200875,201055,"수도"],[201055,201335,"있다고"],[201505,201655,"좀"],[201745,202055,"생각이"],[202055,202515,"들어가지고"],[204025,204235,"이런"],[204245,204395,"거"],[204395,204615,"어때요?"],[204745,204915,"그냥"],[206185,206375,"이렇게"],[206505,206735,"뭔가"]],"textEdited":"좀 어려울 수도 있다고 좀 생각이 들어가지고 이런 거 어때요? 그냥 이렇게 뭔가"},{"start":207430,"end":216030,"text":"실무에서 꼭 쓰지 않더라도 다양한 업무에서 그냥 모두가 쓸 수 있는 거를 한번 생각해 보는 건 어떨지","confidence":0.9729,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[207760,208290,"실무에서"],[208960,209110,"꼭"],[209220,209450,"쓰지"],[209480,209950,"않더라도"],[210220,210570,"다양한"],[210640,211050,"업무에서"],[211120,211290,"그냥"],[211980,212330,"모두가"],[212380,212530,"쓸"],[212530,212670,"수"],[212670,212830,"있는"],[212880,213097,"거를"],[213097,213350,"한번"],[213720,214030,"생각해"],[214030,214290,"보는"],[214290,214410,"건"],[214480,214910,"어떨지"]],"textEdited":"실무에서 꼭 쓰지 않더라도 다양한 업무에서 그냥 모두가 쓸 수 있는 거를 한번 생각해 보는 건 어떨지"},{"start":217103,"end":227320,"text":"지금 우리 미디어 팀 말고도 다른 팀에서도 이제 다양하게 쓸 수 있는 주제를 한번 좀 생각해 보는 것도 좋을 것 같아요.","confidence":0.9791,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[218573,218743,"지금"],[218753,218963,"우리"],[219153,219470,"미디어"],[219470,219603,"팀"],[219653,220083,"말고도"],[220533,220743,"다른"],[220853,221383,"팀에서도"],[221413,221583,"이제"],[221693,222123,"다양하게"],[222213,222363,"쓸"],[222393,222543,"수"],[222593,222803,"있는"],[223133,223483,"주제를"],[223483,223723,"한번"],[223973,224123,"좀"],[225053,225403,"생각해"],[225473,225723,"보는"],[225723,225923,"것도"],[225933,226123,"좋을"],[226123,226230,"것"],[226230,226463,"같아요."]],"textEdited":"지금 우리 미디어 팀 말고도 다른 팀에서도 이제 다양하게 쓸 수 있는 주제를 한번 좀 생각해 보는 것도 좋을 것 같아요."},{"start":231640,"end":236560,"text":"회의 회의는 다 하는데 회의 관련된 건 어떨까요?","confidence":0.9934,"diarization":{"label":"4"},"speaker":{"label":"4","name":"D","edited":false},"words":[[232290,232540,"회의"],[233350,233760,"회의는"],[233850,234000,"다"],[234030,234380,"하는데"],[234750,235000,"회의"],[235050,235420,"관련된"],[235450,235600,"건"],[235630,236040,"어떨까요?"]],"textEdited":"회의 회의는 다 하는데 회의 관련된 건 어떨까요?"},{"start":236560,"end":238630,"text":"괜찮다","confidence":0.8932,"diarization":{"label":"2"},"speaker":{"label":"2","name":"B","edited":false},"words":[[237290,237680,"괜찮다"]],"textEdited":"괜찮다"},{"start":238630,"end":241160,"text":"회의록 작성할 때 참고하면 괜찮은데","confidence":0.952,"diarization":{"label":"3"},"speaker":{"label":"3","name":"C","edited":false},"words":[[239060,239410,"회의록"],[239480,239830,"작성할"],[239830,239950,"때"],[240060,240410,"참고하면"],[240420,240770,"괜찮은데"]],"textEdited":"회의록 작성할 때 참고하면 괜찮은데"},{"start":241160,"end":242470,"text":"어","confidence":0.6216,"diarization":{"label":"2"},"speaker":{"label":"2","name":"B","edited":false},"words":[[241410,241560,"어"]],"textEdited":"어"},{"start":242470,"end":250030,"text":"그러네요. 회의할 때 이제 저희가 회의록은 쓰니까 회의는 누구나 하기도 하고","confidence":0.9777,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[242580,242910,"그러네요."],[243280,243630,"회의할"],[243630,243770,"때"],[243840,244010,"이제"],[244280,244530,"저희가"],[245400,245870,"회의록은"],[245960,246290,"쓰니까"],[247520,247870,"회의는"],[248200,248510,"누구나"],[248540,248850,"하기도"],[248850,249090,"하고"]],"textEdited":"그러네요. 회의할 때 이제 저희가 회의록은 쓰니까 회의는 누구나 하기도 하고"},{"start":251480,"end":253195,"text":"괜찮네요.","confidence":0.9998,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[252130,252560,"괜찮네요."]],"textEdited":"괜찮네요."},{"start":253195,"end":259870,"text":"그럼 회의를 요약해 주는 회의 요약 AI를 만들어 볼까요?","confidence":0.9343,"diarization":{"label":"2"},"speaker":{"label":"2","name":"B","edited":false},"words":[[253645,253835,"그럼"],[253905,254275,"회의를"],[254625,255075,"요약해"],[255125,255395,"주는"],[256685,256915,"회의"],[257145,257415,"요약"],[257765,258335,"AI를"],[258385,258755,"만들어"],[258805,259135,"볼까요?"]],"textEdited":"그럼 회의를 요약해 주는 회의 요약 AI를 만들어 볼까요?"},{"start":259870,"end":264520,"text":"저는 나쁘지 않은 것 같아요. 그 주제가","confidence":0.9508,"diarization":{"label":"1"},"speaker":{"label":"1","name":"A","edited":false},"words":[[261200,261450,"저는"],[261480,261797,"나쁘지"],[261797,261970,"않은"],[261970,262044,"것"],[262044,262270,"같아요."],[263240,263390,"그"],[263400,263810,"주제가"]],"textEdited":"저는 나쁘지 않은 것 같아요. 그 주제가"},{"start":265080,"end":267930,"text":"네 좋은 것 같아요. 회의록 요약.","confidence":0.9695,"diarization":{"label":"4"},"speaker":{"label":"4","name":"D","edited":false},"words":[[265610,265760,"네"],[266050,266240,"좋은"],[266270,266374,"것"],[266374,266620,"같아요."],[266830,267140,"회의록"],[267190,267420,"요약."]],"textEdited":"네 좋은 것 같아요. 회의록 요약."}],"text":"우리가 이제 티앱을 같이 하게 됐는데 주제를 이제 좀 정해야 될 것 같거든요. 주제를 어떤 거를 했으면 좋겠는지 좀 한번 생각해 놓은 게 있으면 조금 얘기를 해 주세요. 저는 클라우드가 좋은 것 같습니다. 요새는 클라우드에서 모든 데이터 처리하고 하는 게 많으니까 클라우드 주제가 좋은 것 같습니다. 찬명 씨는 혹시 생각해 놓은 거 있어요? 요즘 또 트렌드가 빅데이터 쪽이 트렌드도 많고 저희 이제 자격증 같은 것도 이제 빅데이터 쪽 관련된 자격증이 많이 나오고 있거든요. 그래서 저희 그런 자격증 취득하면서 연구 목적으로 빅데이터 쪽 하면은 괜찮을 것 같습니다. 빅데이터도 요새 많이 하니까 좋은 것 같긴 하네요. 근데 이제 제 생각은 우리가 아직 주니어 레벨이니까 그냥 언어 그러니까 시라든지 자바라든지 이런 언어도 좀 공부해 보는 것도 나쁘지 않을 것 같아요. 저는 좀 AI가 해보고 싶은데요. 요즘 AI가 대세잖아요. 챗gpt라든지 AI 해 보면 좀 재미있을 것 같습니다. 확실히 AI 관련해서 기사도 많이 올라오고 그런 것 같아요. AI 나쁘지 않은 것 같은데 네 좋은 것 같습니다. 그렇죠 AI 어때요? 찬민 씨도 AI 어떻게 생각하세요? AI를 한다 그러면 지금 아까 얘기한 것처럼 DPT도 있고 좀 분야가 많은 것 같은데 AI에서 어떤 분야가 좀 더 해야 될지 이거 조금 이거를 좀 정해야 될 것 같습니다. 그러면 아무래도 이게 우리가 회사에서 하는 거니까 업무에 좀 적용하기 좋은 주제를 자꾸 하는 게 맞을 것 같은데요. 우리 팀에서 사용하기 좋은 업무 주제가 뭐 있을까요? AI를 만약에 한다고 하면 제가 프로젝트 학교 다닐 때 썼던 게 이제 AI 쪽 챗봇을 한번 쓴 적이 있었거든요. 그래서 근데 그거는 이제 AI라기보다는 저희가 케이스 바이 케이스를 많이 만들어가지고 이제 사용자가 입력한 그 핵심 단어만 딱 잡아가지고 그거에 관련된 거를 보여주는 챗봇을 했던 적이 있거든요. 챗봇도 하면은 나쁘지 않을 것 같은데 챗봇을 이제 지금 저희 사용자들이 물어봤을 때 이거를 답변을 해 주는 거를 하는 것도 나쁘지 않을 것 같습니다. 챗봇은 그럼 우리 팀에서만 쓸 수 있는 걸 말하는 건가? 어쨌든 연구 목적이면은 크게 문제없지 않을까 싶은데 이건 단순하게 의견이라서 그냥 이런 것도 해봤다라고 얘기드린 거예요. 근데 또 얘기를 들어보니까 그러면은 좀 뭔가 챗봇이라고 하면은 일단 다양한 업무에 좀 적용하기에는 좀 주제가 좀 어려울 수도 있다고 좀 생각이 들어가지고 이런 거 어때요? 그냥 이렇게 뭔가 실무에서 꼭 쓰지 않더라도 다양한 업무에서 그냥 모두가 쓸 수 있는 거를 한번 생각해 보는 건 어떨지 지금 우리 미디어 팀 말고도 다른 팀에서도 이제 다양하게 쓸 수 있는 주제를 한번 좀 생각해 보는 것도 좋을 것 같아요. 회의 회의는 다 하는데 회의 관련된 건 어떨까요? 괜찮다 회의록 작성할 때 참고하면 괜찮은데 어 그러네요. 회의할 때 이제 저희가 회의록은 쓰니까 회의는 누구나 하기도 하고 괜찮네요. 그럼 회의를 요약해 주는 회의 요약 AI를 만들어 볼까요? 저는 나쁘지 않은 것 같아요. 그 주제가 네 좋은 것 같아요. 회의록 요약.","confidence":0.9527962,"speakers":[{"label":"1","name":"A","edited":false},{"label":"2","name":"B","edited":false},{"label":"3","name":"C","edited":false},{"label":"4","name":"D","edited":false}],"events":[],"eventTypes":[]}'
    
    # 인증서 파일 경로
    # cert_file_path = 'C:/Users/User/Downloads/Clova_Util/ncloud_CA.pem'

    def req_url(self, url, completion, callback=None, userdata=None, forbiddens=None, boostings=None, wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'url': url,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'sed': sed,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        return requests.post(headers=headers,
                             url=self.invoke_url + '/recognizer/url',
                             data=json.dumps(request_body).encode('UTF-8'), verify=False)

    def req_object_storage(self, data_key, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                           wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'dataKey': data_key,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'sed': sed,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        return requests.post(headers=headers,
                             url=self.invoke_url + '/recognizer/object-storage',
                             data=json.dumps(request_body).encode('UTF-8'), verify=False)

    def req_upload(self, file, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                   wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'sed': sed,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        print(json.dumps(request_body, ensure_ascii=False).encode('UTF-8'))
        files = {
            'media': open(file, 'rb'),
            'params': (None, json.dumps(request_body, ensure_ascii=False).encode('UTF-8'), 'application/json')
        }
        response = requests.post(headers=headers, url=self.invoke_url + '/recognizer/upload', files=files, verify=False)
        return response

    def getSttSpeakResult(self,save_path):
        
        # res = ClovaSpeechClient().req_upload(file=save_path, completion='sync') #파일 업로드
        # json_obj = json.loads(res.text)
        json_obj = json.loads(self.res)
        
        #graph를 위한 result
        speaker_result = [] 
        speakers_arr = json_obj['speakers']
        segments_arr = json_obj['segments']

        for speaker in speakers_arr:
            tmp = speaker['label']
            text_edited = ''

            for segment in segments_arr:
                speaker_label = segment['speaker']['label']
                if tmp == speaker_label:
                    puct_delete = segment['textEdited'].replace('"', '').replace('.', ' ')
                    text_edited += puct_delete + ' '  

            speaker_result.append(text_edited.strip())  

        # 결과 출력 (맨 마지막 쉼표 제거)
        #print(', '.join(speaker_result))
        #print('\n'.join(stt_result))
        return speaker_result
    
    def getSttAllResult(self,save_path):
        
        # res = ClovaSpeechClient().req_upload(file=save_path, completion='sync') #파일 업로드
        # json_obj = json.loads(res.text)
        json_obj = json.loads(self.res)
        
        #회의록 녹취록 전문 위한 result
        stt_result = []

        segments_arr = json_obj['segments']
      
        for segment in segments_arr:
            speaker_label = segment['speaker']['label']
            stt_result.append(('화자'+speaker_label+': '+segment['textEdited']).strip())        
        
        return stt_result
    
    def getSttOrigin(self,save_path):
        
        res = ClovaSpeechClient().req_upload(file=save_path, completion='sync') #파일 업로드
        json_obj = json.loads(res.text)
        # json_obj = json.loads(self.res)
        
        result = json_obj['text']
        
        return result
    
    def getSttAllResultDf(self,save_path):

        print("Uploading file:", save_path)
        
        res = ClovaSpeechClient().req_upload(file=save_path, completion='sync') #파일 업로드

        print("Upload response:", res.text)

        try:
            json_obj = json.loads(res.text)
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            return None
        # json_obj = json.loads(res.text)
        # json_obj = json.loads(self.res)
        
        #회의록 녹취록 전문 위한 result
        result = []

        segments_arr = json_obj['segments']

         print("Segments array:", segments_arr)
      
        for segment in segments_arr:
            stt_result = []
            speaker_label = segment['speaker']['label']
            stt_result.append('화자'+speaker_label)    
            stt_result.append(segment['textEdited'])  
            result.append(stt_result)
        
        return result
        
