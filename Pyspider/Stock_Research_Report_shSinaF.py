#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-08-31 12:31:17
# Project: Stock_Research_Report_shSinaF

from pyspider.libs.base_handler import *

stocklist = [["信达增利","sh166105"],
["R003","sh201000"],["R007","sh201001"],["R014","sh201002"],["R028","sh201003"],["R091","sh201004"],["R182","sh201005"],["R001","sh201008"],
["R002","sh201009"],["R004","sh201010"],["RC001","sh202001"],["RC003","sh202003"],["RC007","sh202007"],["0501R007","sh203007"],["0501R028","sh203008"],
["0501R091","sh203009"],["0504R007","sh203016"],["0504R028","sh203017"],["0504R091","sh203018"],["0505R007","sh203019"],["0505R028","sh203020"],["0505R091","sh203021"],
["0509R007","sh203031"],["0509R028","sh203032"],["0509R091","sh203033"],["0512R007","sh203040"],["0512R028","sh203041"],["0512R091","sh203042"],["0513R007","sh203043"],
["0513R028","sh203044"],["0513R091","sh203045"],["0601R007","sh203049"],["0601R028","sh203050"],["0601R091","sh203051"],["0603R007","sh203052"],["0603R028","sh203053"],
["0603R091","sh203054"],["GC001","sh204001"],["GC002","sh204002"],["GC003","sh204003"],["GC004","sh204004"],["GC007","sh204007"],["GC014","sh204014"],["GC028","sh204028"],
["GC091","sh204091"],["GC182","sh204182"],["基金金泰","sh500001"],["基金泰和","sh500002"],["基金安信","sh500003"],["基金汉盛","sh500005"],["基金裕阳","sh500006"],
["基金景阳","sh500007"],["基金兴华","sh500008"],["基金安顺","sh500009"],["基金金鑫","sh500011"],["基金汉兴","sh500015"],["基金兴和","sh500018"],["基金科讯","sh500029"],
["基金通乾","sh500038"],["基金科瑞","sh500056"],["基金银丰","sh500058"],["500等权","sh502000"],["500等权A","sh502001"],["500等权B","sh502002"],["国企改革","sh502006"],
["国企改A","sh502007"],["国企改B","sh502008"],["一带一路","sh502013"],["一带一A","sh502014"],["一带一B","sh502015"],["国金50","sh502020"],["国金50A","sh502021"],
["国金50B","sh502022"],["互联金融","sh502036"],["网金A","sh502037"],["网金B","sh502038"],["50分级","sh502048"],["上证50A","sh502049"],["上证50B","sh502050"],
["嘉实元和","sh505888"],["治理ETF","sh510010"],["超大ETF","sh510020"],["价值ETF","sh510030"],["50ETF","sh510050"],["央企ETF","sh510060"],["央企申赎","sh510061"],
["民企ETF","sh510070"],["责任ETF","sh510090"],["周期ETF","sh510110"],["非周ETF","sh510120"],["中盘ETF","sh510130"],["招商上证消费80","sh510150"],["小康ETF","sh510160"],
["商品ETF","sh510170"],["180ETF","sh510180"],["龙头ETF","sh510190"],["综指ETF","sh510210"],["中小ETF","sh510220"],["金融ETF","sh510230"],["新兴ETF","sh510260"],
["国企ETF","sh510270"],["成长ETF","sh510280"],["380ETF","sh510290"],["300ETF","sh510300"],["HS300ETF","sh510310"],["华夏300","sh510330"],["资源ETF","sh510410"],
["180EWETF","sh510420"],["50等权","sh510430"],["500沪市ETF","sh510440"],["180高ETF","sh510450"],["500ETF","sh510500"],["广发500","sh510510"],["诺安500","sh510520"],
["国寿500","sh510560"],["能源行业","sh510610"],["材料行业","sh510620"],["消费行业","sh510630"],["金融行业","sh510650"],["医药行业","sh510660"],["万家380","sh510680"],
["百强ETF","sh510700"],["上50ETF","sh510710"],["红利ETF","sh510880"],["H股ETF","sh510900"],["国债ETF","sh511010"],["企债ETF","sh511210"],["城投ETF","sh511220"],
["易货币","sh511800"],["博时货币","sh511860"],["银华日利","sh511880"],["华宝添益","sh511990"],["医药ETF","sh512010"],["非银ETF","sh512070"],["景顺食品","sh512210"],
["景顺TMT","sh512220"],["景顺医药","sh512230"],["500医药","sh512300"],["500工业","sh512310"],["500原料","sh512340"],["中证500","sh512500"],["ETF500","sh512510"],
["主要消费","sh512600"],["医药卫生","sh512610"],["金融地产","sh512640"],["MSCIA股","sh512990"],["德国30","sh513030"],["纳指ETF","sh513100"],["标普500","sh513500"],
["恒指ETF","sh513600"],["恒生通","sh513660"],["国泰黄金","sh518800"],["黄金ETF","sh518880"],["云化CWB1","sh580012"],["武钢CWB1","sh580013"],["深高CWB1","sh580014"],
["上汽CWB1","sh580016"],["赣粤CWB1","sh580017"],["石化CWB1","sh580019"],["上港CWB1","sh580020"],["青啤CWB1","sh580021"],["国电CWB1","sh580022"],["康美CWB1","sh580023"],
["宝钢CWB1","sh580024"],["葛洲CWB1","sh580025"],["江铜CWB1","sh580026"],["长虹CWB1","sh580027"],["浦发银行","sh600000"],["邯郸钢铁","sh600001"],["齐鲁石化","sh600002"],
["ST东北高","sh600003"],["白云机场","sh600004"],["武钢股份","sh600005"],["东风汽车","sh600006"],["中国国贸","sh600007"],["首创股份","sh600008"],["上海机场","sh600009"],
["包钢股份","sh600010"],["华能国际","sh600011"],["皖通高速","sh600012"],["华夏银行","sh600015"],["民生银行","sh600016"],["日照港","sh600017"],["上港集团","sh600018"],
["宝钢股份","sh600019"],["中原高速","sh600020"],["上海电力","sh600021"],["山东钢铁","sh600022"],["浙能电力","sh600023"],["中海发展","sh600026"],["华电国际","sh600027"],
["中国石化","sh600028"],["南方航空","sh600029"],["中信证券","sh600030"],["三一重工","sh600031"],["福建高速","sh600033"],["楚天高速","sh600035"],["招商银行","sh600036"],
["歌华有线","sh600037"],["中直股份","sh600038"],["四川路桥","sh600039"],["保利地产","sh600048"],["中国联通","sh600050"],["宁波联合","sh600051"],["浙江广厦","sh600052"],
["中江地产","sh600053"],["黄山旅游","sh600054"],["华润万东","sh600055"],["中国医药","sh600056"],["象屿股份","sh600057"],["五矿发展","sh600058"],["古越龙山","sh600059"],
["海信电器","sh600060"],["国投安信","sh600061"],["华润双鹤","sh600062"],["皖维高新","sh600063"],["南京高科","sh600064"],["*ST联谊","sh600065"],["宇通客车","sh600066"],
["冠城大通","sh600067"],["葛洲坝","sh600068"],["*ST银鸽","sh600069"],["浙江富润","sh600070"],["*ST光学","sh600071"],["钢构工程","sh600072"],["上海梅林","sh600073"],
["保千里","sh600074"],["新疆天业","sh600075"],["青鸟华光","sh600076"],["宋都股份","sh600077"],["澄星股份","sh600078"],["人福医药","sh600079"],["金花股份","sh600080"],
["东风科技","sh600081"],["海泰发展","sh600082"],["博信股份","sh600083"],["中葡股份","sh600084"],["同仁堂","sh600085"],["东方金钰","sh600086"],["退市长油","sh600087"],
["中视传媒","sh600088"],["特变电工","sh600089"],["啤酒花","sh600090"],["*ST明科","sh600091"],["S*ST精密","sh600092"],["禾嘉股份","sh600093"],["大名城","sh600094"],
["哈高科","sh600095"],["云天化","sh600096"],["开创国际","sh600097"],["广州发展","sh600098"],["林海股份","sh600099"],["同方股份","sh600100"],["明星电力","sh600101"],
["莱钢股份","sh600102"],["青山纸业","sh600103"],["上汽集团","sh600104"],["永鼎股份","sh600105"],["重庆路桥","sh600106"],["美尔雅","sh600107"],["亚盛集团","sh600108"],
["国金证券","sh600109"],["中科英华","sh600110"],["北方稀土","sh600111"],["天成控股","sh600112"],["浙江东日","sh600113"],["东睦股份","sh600114"],["东方航空","sh600115"],
["三峡水利","sh600116"],["西宁特钢","sh600117"],["中国卫星","sh600118"],["长江投资","sh600119"],["浙江东方","sh600120"],["郑州煤电","sh600121"],["宏图高科","sh600122"],
["兰花科创","sh600123"],["铁龙物流","sh600125"],["杭钢股份","sh600126"],["金健米业","sh600127"],["弘业股份","sh600128"],["太极集团","sh600129"],["波导股份","sh600130"],
["岷江水电","sh600131"],["重庆啤酒","sh600132"],["东湖高新","sh600133"],["乐凯胶片","sh600135"],["道博股份","sh600136"],["浪莎股份","sh600137"],["中青旅","sh600138"],
["西部资源","sh600139"],["兴发集团","sh600141"],["金发科技","sh600143"],["*ST新亿","sh600145"],["大元股份","sh600146"],["长春一东","sh600148"],["廊坊发展","sh600149"],
["中国船舶","sh600150"],["航天机电","sh600151"],["维科精华","sh600152"],["建发股份","sh600153"],["宝硕股份","sh600155"],["华升股份","sh600156"],["永泰能源","sh600157"],
["中体产业","sh600158"],["大龙地产","sh600159"],["巨化股份","sh600160"],["天坛生物","sh600161"],["香江控股","sh600162"],["*ST南纸","sh600163"],["新日恒力","sh600165"],
["福田汽车","sh600166"],["联美控股","sh600167"],["武汉控股","sh600168"],["太原重工","sh600169"],["上海建工","sh600170"],["上海贝岭","sh600171"],["黄河旋风","sh600172"],
["卧龙地产","sh600173"],["美都能源","sh600175"],["中国巨石","sh600176"],["雅戈尔","sh600177"],["东安动力","sh600178"],["黑化股份","sh600179"],["瑞茂通","sh600180"],
["S*ST云大","sh600181"],["S佳通","sh600182"],["生益科技","sh600183"],["光电股份","sh600184"],["格力地产","sh600185"],["莲花味精","sh600186"],["国中水务","sh600187"],
["兖州煤业","sh600188"],["吉林森工","sh600189"],["锦州港","sh600190"],["华资实业","sh600191"],["长城电工","sh600192"],["创兴资源","sh600193"],["中牧股份","sh600195"],
["复星医药","sh600196"],["伊力特","sh600197"],["大唐电信","sh600198"],["金种子酒","sh600199"],["江苏吴中","sh600200"],["金宇集团","sh600201"],["哈空调","sh600202"],
["福日电子","sh600203"],["S山东铝","sh600205"],["有研新材","sh600206"],["安彩高科","sh600207"],["新湖中宝","sh600208"],["罗顿发展","sh600209"],["紫江企业","sh600210"],
["西藏药业","sh600211"],["江泉实业","sh600212"],["亚星客车","sh600213"],["长春经开","sh600215"],["浙江医药","sh600216"],["*ST秦岭","sh600217"],["全柴动力","sh600218"],
["南山铝业","sh600219"],["江苏阳光","sh600220"],["海南航空","sh600221"],["太龙药业","sh600222"],["鲁商置业","sh600223"],["天津松江","sh600225"],["升华拜克","sh600226"],
["赤天化","sh600227"],["昌九生化","sh600228"],["青岛碱业","sh600229"],["沧州大化","sh600230"],["凌钢股份","sh600231"],["金鹰股份","sh600232"],["大杨创世","sh600233"],
["山水文化","sh600234"],["民丰特纸","sh600235"],["桂冠电力","sh600236"],["铜峰电子","sh600237"],["海南椰岛","sh600238"],["云南城投","sh600239"],["华业资本","sh600240"],
["时代万恒","sh600241"],["*ST中昌","sh600242"],["青海华鼎","sh600243"],["万通地产","sh600246"],["*ST成城","sh600247"],["延长化建","sh600248"],["两面针","sh600249"],
["南纺股份","sh600250"],["冠农股份","sh600251"],["中恒集团","sh600252"],["天方药业","sh600253"],["鑫科材料","sh600255"],["广汇能源","sh600256"],["大湖股份","sh600257"],
["首旅酒店","sh600258"],["广晟有色","sh600259"],["凯乐科技","sh600260"],["阳光照明","sh600261"],["北方股份","sh600262"],["路桥建设","sh600263"],["ST景谷","sh600265"],
["北京城建","sh600266"],["海正药业","sh600267"],["国电南自","sh600268"],["赣粤高速","sh600269"],["外运发展","sh600270"],["航天信息","sh600271"],["开开实业","sh600272"],
["嘉化能源","sh600273"],["武昌鱼","sh600275"],["恒瑞医药","sh600276"],["亿利能源","sh600277"],["东方创业","sh600278"],["重庆港九","sh600279"],["中央商场","sh600280"],
["太化股份","sh600281"],["南钢股份","sh600282"],["钱江水利","sh600283"],["浦东建设","sh600284"],["羚锐制药","sh600285"],["S*ST国瓷","sh600286"],["江苏舜天","sh600287"],
["大恒科技","sh600288"],["亿阳信通","sh600289"],["华仪电气","sh600290"],["西水股份","sh600291"],["中电远达","sh600292"],["三峡新材","sh600293"],["鄂尔多斯","sh600295"],
["S兰铝","sh600296"],["广汇汽车","sh600297"],["安琪酵母","sh600298"],["蓝星新材","sh600299"],["维维股份","sh600300"],["*ST南化","sh600301"],["标准股份","sh600302"],
["曙光股份","sh600303"],["恒顺醋业","sh600305"],["商业城","sh600306"],["酒钢宏兴","sh600307"],["华泰股份","sh600308"],["万华化学","sh600309"],["桂东电力","sh600310"],
["荣华实业","sh600311"],["平高电气","sh600312"],["农发种业","sh600313"],["上海家化","sh600315"],["洪都航空","sh600316"],["营口港","sh600317"],["巢东股份","sh600318"],
["亚星化学","sh600319"],["振华重工","sh600320"],["国栋建设","sh600321"],["天房发展","sh600322"],["瀚蓝环境","sh600323"],["华发股份","sh600325"],["西藏天路","sh600326"],
["大东方","sh600327"],["兰太实业","sh600328"],["中新药业","sh600329"],["天通股份","sh600330"],["宏达股份","sh600331"],["白云山","sh600332"],["长春燃气","sh600333"],
["国机汽车","sh600335"],["澳柯玛","sh600336"],["美克家居","sh600337"],["西藏珠峰","sh600338"],["天利高新","sh600339"],["华夏幸福","sh600340"],["航天动力","sh600343"],
["长江通信","sh600345"],["大橡塑","sh600346"],["阳泉煤业","sh600348"],["富通昭和","sh600349"],["山东高速","sh600350"],["亚宝药业","sh600351"],["浙江龙盛","sh600352"],
["旭光股份","sh600353"],["敦煌种业","sh600354"],["精伦电子","sh600355"],["恒丰纸业","sh600356"],["承德钒钛","sh600357"],["国旅联合","sh600358"],["新农开发","sh600359"],
["华微电子","sh600360"],["华联综超","sh600361"],["江西铜业","sh600362"],["联创光电","sh600363"],["通葡股份","sh600365"],["宁波韵升","sh600366"],["红星发展","sh600367"],
["五洲交通","sh600368"],["西南证券","sh600369"],["三房巷","sh600370"],["万向德农","sh600371"],["中航电子","sh600372"],["中文传媒","sh600373"],["华菱星马","sh600375"],
["首开股份","sh600376"],["宁沪高速","sh600377"],["天科股份","sh600378"],["宝光股份","sh600379"],["健康元","sh600380"],["青海春天","sh600381"],["广东明珠","sh600382"],
["金地集团","sh600383"],["山东金泰","sh600385"],["北巴传媒","sh600386"],["海越股份","sh600387"],["龙净环保","sh600388"],["江山股份","sh600389"],["金瑞科技","sh600390"],
["成发科技","sh600391"],["盛和资源","sh600392"],["东华实业","sh600393"],["盘江股份","sh600395"],["金山股份","sh600396"],["安源煤业","sh600397"],["海澜之家","sh600398"],
["抚顺特钢","sh600399"],["红豆股份","sh600400"],["*ST海润","sh600401"],["大有能源","sh600403"],["动力源","sh600405"],["国电南瑞","sh600406"],["*ST安泰","sh600408"],
["三友化工","sh600409"],["华胜天成","sh600410"],["小商品城","sh600415"],["湘电股份","sh600416"],["江淮汽车","sh600418"],["天润乳业","sh600419"],["现代制药","sh600420"],
["仰帆控股","sh600421"],["昆药集团","sh600422"],["柳化股份","sh600423"],["青松建化","sh600425"],["华鲁恒升","sh600426"],["中远航运","sh600428"],["三元股份","sh600429"],
["吉恩镍业","sh600432"],["冠豪高新","sh600433"],["北方导航","sh600435"],["片仔癀","sh600436"],["通威股份","sh600438"],["瑞贝卡","sh600439"],["*ST国通","sh600444"],
["金证股份","sh600446"],["华纺股份","sh600448"],["宁夏建材","sh600449"],["涪陵电力","sh600452"],["博通股份","sh600455"],["宝钛股份","sh600456"],["时代新材","sh600458"],
["贵研铂业","sh600459"],["士兰微","sh600460"],["洪城水业","sh600461"],["石岘纸业","sh600462"],["空港股份","sh600463"],["蓝光发展","sh600466"],["好当家","sh600467"],
["百利电气","sh600468"],["风神股份","sh600469"],["六国化工","sh600470"],["包头铝业","sh600472"],["华光股份","sh600475"],["湘邮科技","sh600476"],["杭萧钢构","sh600477"],
["科力远","sh600478"],["千金药业","sh600479"],["凌云股份","sh600480"],["双良节能","sh600481"],["风帆股份","sh600482"],["福建南纺","sh600483"],["信威集团","sh600485"],
["扬农化工","sh600486"],["亨通光电","sh600487"],["天药股份","sh600488"],["中金黄金","sh600489"],["鹏欣资源","sh600490"],["龙元建设","sh600491"],["凤竹纺织","sh600493"],
["晋西车轴","sh600495"],["精工钢构","sh600496"],["驰宏锌锗","sh600497"],["烽火通信","sh600498"],["科达洁能","sh600499"],["中化国际","sh600500"],["航天晨光","sh600501"],
["安徽水利","sh600502"],["华丽家族","sh600503"],["西昌电力","sh600505"],["香梨股份","sh600506"],["方大特钢","sh600507"],["上海能源","sh600508"],["天富能源","sh600509"],
["黑牡丹","sh600510"],["国药股份","sh600511"],["腾达建设","sh600512"],["联环药业","sh600513"],["海岛建设","sh600515"],["方大炭素","sh600516"],["置信电气","sh600517"],
["康美药业","sh600518"],["贵州茅台","sh600519"],["中发科技","sh600520"],["华海药业","sh600521"],["中天科技","sh600522"],["贵航股份","sh600523"],["长园集团","sh600525"],
["菲达环保","sh600526"],["江南高纤","sh600527"],["中铁二局","sh600528"],["山东药玻","sh600529"],["交大昂立","sh600530"],["豫光金铅","sh600531"],["宏达矿业","sh600532"],
["栖霞建设","sh600533"],["天士力","sh600535"],["中国软件","sh600536"],["亿晶光电","sh600537"],["国发股份","sh600538"],["*ST狮头","sh600539"],["新赛股份","sh600540"],
["莫高股份","sh600543"],["新疆城建","sh600545"],["山煤国际","sh600546"],["山东黄金","sh600547"],["深高速","sh600548"],["厦门钨业","sh600549"],["保变电气","sh600550"],
["时代出版","sh600551"],["方兴科技","sh600552"],["太行水泥","sh600553"],["九龙山","sh600555"],["慧球科技","sh600556"],["康缘药业","sh600557"],["大西洋","sh600558"],
["老白干酒","sh600559"],["金自天正","sh600560"],["江西长运","sh600561"],["国睿科技","sh600562"],["法拉电子","sh600563"],["迪马股份","sh600565"],["济川药业","sh600566"],
["山鹰纸业","sh600567"],["中珠控股","sh600568"],["安阳钢铁","sh600569"],["恒生电子","sh600570"],["信雅达","sh600571"],["康恩贝","sh600572"],["惠泉啤酒","sh600573"],
["皖江物流","sh600575"],["万好万家","sh600576"],["精达股份","sh600577"],["京能电力","sh600578"],["天华院","sh600579"],["卧龙电气","sh600580"],["八一钢铁","sh600581"],
["天地科技","sh600582"],["海油工程","sh600583"],["长电科技","sh600584"],["海螺水泥","sh600585"],["金晶科技","sh600586"],["新华医疗","sh600587"],["用友网络","sh600588"],
["广东榕泰","sh600589"],["泰豪科技","sh600590"],["*ST上航","sh600591"],["龙溪股份","sh600592"],["大连圣亚","sh600593"],["益佰制药","sh600594"],["中孚实业","sh600595"],
["新安股份","sh600596"],["光明乳业","sh600597"],["北大荒","sh600598"],["熊猫金控","sh600599"],["青岛啤酒","sh600600"],["方正科技","sh600601"],["仪电电子","sh600602"],
["大洲兴业","sh600603"],["市北高新","sh600604"],["汇通能源","sh600605"],["金丰投资","sh600606"],["上实医药","sh600607"],["*ST沪科","sh600608"],["金杯汽车","sh600609"],
["中毅达","sh600610"],["大众交通","sh600611"],["老凤祥","sh600612"],["神奇制药","sh600613"],["鼎立股份","sh600614"],["丰华股份","sh600615"],["金枫酒业","sh600616"],
["国新能源","sh600617"],["氯碱化工","sh600618"],["海立股份","sh600619"],["天宸股份","sh600620"],["华鑫股份","sh600621"],["嘉宝集团","sh600622"],["双钱股份","sh600623"],
["复旦复华","sh600624"],["PT水仙","sh600625"],["申达股份","sh600626"],["上电股份","sh600627"],["新世界","sh600628"],["棱光实业","sh600629"],["龙头股份","sh600630"],
["百联股份","sh600631"],["华联商厦","sh600632"],["浙报传媒","sh600633"],["中技控股","sh600634"],["大众公用","sh600635"],["三爱富","sh600636"],["东方明珠","sh600637"],
["新黄浦","sh600638"],["浦东金桥","sh600639"],["号百控股","sh600640"],["万业企业","sh600641"],["申能股份","sh600642"],["爱建股份","sh600643"],["*ST乐电","sh600644"],
["中源协和","sh600645"],["ST国嘉","sh600646"],["同达创业","sh600647"],["外高桥","sh600648"],["城投控股","sh600649"],["锦江投资","sh600650"],["飞乐音响","sh600651"],
["游久游戏","sh600652"],["申华控股","sh600653"],["中安消","sh600654"],["豫园商城","sh600655"],["*ST博元","sh600656"],["信达地产","sh600657"],["电子城","sh600658"],
["*ST花雕","sh600659"],["福耀玻璃","sh600660"],["新南洋","sh600661"],["强生控股","sh600662"],["陆家嘴","sh600663"],["哈药股份","sh600664"],["天地源","sh600665"],
["奥瑞德","sh600666"],["太极实业","sh600667"],["尖峰集团","sh600668"],["*ST鞍成","sh600669"],["*ST斯达","sh600670"],["天目药业","sh600671"],["*ST华圣","sh600672"],
["东阳光科","sh600673"],["川投能源","sh600674"],["中华企业","sh600675"],["交运股份","sh600676"],["航天通信","sh600677"],["四川金顶","sh600678"],["金山开发","sh600679"],
["上海普天","sh600680"],["万鸿集团","sh600681"],["南京新百","sh600682"],["京投银泰","sh600683"],["珠江实业","sh600684"],["中船防务","sh600685"],["金龙汽车","sh600686"],
["刚泰控股","sh600687"],["上海石化","sh600688"],["上海三毛","sh600689"],["青岛海尔","sh600690"],["*ST阳化","sh600691"],["亚通股份","sh600692"],["东百集团","sh600693"],
["大商股份","sh600694"],["绿庭投资","sh600695"],["匹凸匹","sh600696"],["欧亚集团","sh600697"],["湖南天雁","sh600698"],["均胜电子","sh600699"],["*ST数码","sh600700"],
["工大高新","sh600701"],["沱牌舍得","sh600702"],["三安光电","sh600703"],["物产中大","sh600704"],["中航资本","sh600705"],["曲江文旅","sh600706"],["彩虹股份","sh600707"],
["海博股份","sh600708"],["ST生态","sh600709"],["*ST常林","sh600710"],["盛屯矿业","sh600711"],["南宁百货","sh600712"],["南京医药","sh600713"],["金瑞矿业","sh600714"],
["*ST松辽","sh600715"],["凤凰股份","sh600716"],["天津港","sh600717"],["东软集团","sh600718"],["大连热电","sh600719"],["祁连山","sh600720"],["百花村","sh600721"],
["*ST金化","sh600722"],["首商股份","sh600723"],["宁波富达","sh600724"],["云维股份","sh600725"],["华电能源","sh600726"],["鲁北化工","sh600727"],["佳都科技","sh600728"],
["重庆百货","sh600729"],["中国高科","sh600730"],["湖南海利","sh600731"],["*ST新梅","sh600732"],["S前锋","sh600733"],["实达集团","sh600734"],["新华锦","sh600735"],
["苏州高新","sh600736"],["中粮屯河","sh600737"],["兰州民百","sh600738"],["辽宁成大","sh600739"],["山西焦化","sh600740"],["华域汽车","sh600741"],["一汽富维","sh600742"],
["华远地产","sh600743"],["华银电力","sh600744"],["中茵股份","sh600745"],["江苏索普","sh600746"],["大连控股","sh600747"],["上实发展","sh600748"],["西藏旅游","sh600749"],
["江中药业","sh600750"],["天海投资","sh600751"],["*ST哈慈","sh600752"],["东方银星","sh600753"],["锦江股份","sh600754"],["厦门国贸","sh600755"],["浪潮软件","sh600756"],
["长江传媒","sh600757"],["红阳能源","sh600758"],["洲际油气","sh600759"],["中航黑豹","sh600760"],["安徽合力","sh600761"],["S*ST金荔","sh600762"],["通策医疗","sh600763"],
["中电广通","sh600764"],["中航重机","sh600765"],["园城黄金","sh600766"],["运盛医疗","sh600767"],["宁波富邦","sh600768"],["祥龙电业","sh600769"],["综艺股份","sh600770"],
["广誉远","sh600771"],["S*ST龙昌","sh600772"],["西藏城投","sh600773"],["汉商集团","sh600774"],["南京熊猫","sh600775"],["东方通信","sh600776"],["新潮实业","sh600777"],
["友好集团","sh600778"],["*ST水井","sh600779"],["通宝能源","sh600780"],["辅仁药业","sh600781"],["新钢股份","sh600782"],["鲁信创投","sh600783"],["鲁银投资","sh600784"],
["新华百货","sh600785"],["东方锅炉","sh600786"],["中储股份","sh600787"],["*ST达曼","sh600788"],["鲁抗医药","sh600789"],["轻纺城","sh600790"],["京能置业","sh600791"],
["云煤能源","sh600792"],["ST宜纸","sh600793"],["保税科技","sh600794"],["国电电力","sh600795"],["钱江生化","sh600796"],["浙大网新","sh600797"],["宁波海运","sh600798"],
["*ST龙科","sh600799"],["天津磁卡","sh600800"],["华新水泥","sh600801"],["福建水泥","sh600802"],["新奥股份","sh600803"],["鹏博士","sh600804"],["悦达投资","sh600805"],
["昆明机床","sh600806"],["天业股份","sh600807"],["马钢股份","sh600808"],["山西汾酒","sh600809"],["神马股份","sh600810"],["东方集团","sh600811"],["华北制药","sh600812"],
["ST鞍一工","sh600813"],["杭州解百","sh600814"],["厦工股份","sh600815"],["安信信托","sh600816"],["ST宏盛","sh600817"],["中路股份","sh600818"],["耀皮玻璃","sh600819"],
["隧道股份","sh600820"],["津劝业","sh600821"],["上海物贸","sh600822"],["世茂股份","sh600823"],["益民集团","sh600824"],["新华传媒","sh600825"],["兰生股份","sh600826"],
["百联股份","sh600827"],["成商集团","sh600828"],["人民同泰","sh600829"],["香溢融通","sh600830"],["广电网络","sh600831"],["东方明珠","sh600832"],["第一医药","sh600833"],
["申通地铁","sh600834"],["上海机电","sh600835"],["界龙实业","sh600836"],["海通证券","sh600837"],["上海九百","sh600838"],["四川长虹","sh600839"],["新湖创业","sh600840"],
["上柴股份","sh600841"],["中西药业","sh600842"],["上工申贝","sh600843"],["丹化科技","sh600844"],["宝信软件","sh600845"],["同济科技","sh600846"],["万里股份","sh600847"],
["自仪股份","sh600848"],["上药转换","sh600849"],["华东电脑","sh600850"],["海欣股份","sh600851"],["*ST中川","sh600852"],["龙建股份","sh600853"],["春兰股份","sh600854"],
["航天长峰","sh600855"],["长百集团","sh600856"],["宁波中百","sh600857"],["银座股份","sh600858"],["王府井","sh600859"],["京城股份","sh600860"],["北京城乡","sh600861"],
["南通科技","sh600862"],["内蒙华电","sh600863"],["哈投股份","sh600864"],["百大集团","sh600865"],["星湖科技","sh600866"],["通化东宝","sh600867"],["梅雁吉祥","sh600868"],
["智慧能源","sh600869"],["*ST厦华","sh600870"],["石化油服","sh600871"],["中炬高新","sh600872"],["梅花生物","sh600873"],["创业环保","sh600874"],["东方电气","sh600875"],
["洛阳玻璃","sh600876"],["中国嘉陵","sh600877"],["*ST北科","sh600878"],["航天电子","sh600879"],["博瑞传播","sh600880"],["亚泰集团","sh600881"],["华联矿业","sh600882"],
["博闻科技","sh600883"],["杉杉股份","sh600884"],["宏发股份","sh600885"],["国投电力","sh600886"],["伊利股份","sh600887"],["新疆众和","sh600888"],["南京化纤","sh600889"],
["中房股份","sh600890"],["秋林集团","sh600891"],["宝诚股份","sh600892"],["中航动力","sh600893"],["广日股份","sh600894"],["张江高科","sh600895"],["中海海盛","sh600896"],
["厦门空港","sh600897"],["三联商社","sh600898"],["*ST信联","sh600899"],["长江电力","sh600900"],["重庆燃气","sh600917"],["东方证券","sh600958"],["江苏有线","sh600959"],
["渤海活塞","sh600960"],["株冶集团","sh600961"],["*ST中鲁","sh600962"],["岳阳林纸","sh600963"],["福成五丰","sh600965"],["博汇纸业","sh600966"],["北方创业","sh600967"],
["郴电国际","sh600969"],["中材国际","sh600970"],["恒源煤电","sh600971"],["宝胜股份","sh600973"],["新五丰","sh600975"],["健民集团","sh600976"],["宜华木业","sh600978"],
["广安爱众","sh600979"],["北矿磁材","sh600980"],["汇鸿股份","sh600981"],["宁波热电","sh600982"],["惠而浦","sh600983"],["*ST建机","sh600984"],["雷鸣科化","sh600985"],
["科达股份","sh600986"],["航民股份","sh600987"],["赤峰黄金","sh600988"],["四创电子","sh600990"],["广汽长丰","sh600991"],["贵绳股份","sh600992"],["马应龙","sh600993"],
["文山电力","sh600995"],["开滦股份","sh600997"],["九州通","sh600998"],["招商证券","sh600999"],["唐山港","sh601000"],["大同煤业","sh601001"],["晋亿实业","sh601002"],
["柳钢股份","sh601003"],["重庆钢铁","sh601005"],["大秦铁路","sh601006"],["金陵饭店","sh601007"],["连云港","sh601008"],["南京银行","sh601009"],["文峰股份","sh601010"],
["宝泰隆","sh601011"],["隆基股份","sh601012"],["陕西黑猫","sh601015"],["节能风电","sh601016"],["宁波港","sh601018"],["春秋航空","sh601021"],["玉龙股份","sh601028"],
["一拖股份","sh601038"],["赛轮金宇","sh601058"],["西部黄金","sh601069"],["中国神华","sh601088"],["中南传媒","sh601098"],["太平洋","sh601099"],["恒立油缸","sh601100"],
["昊华能源","sh601101"],["中国一重","sh601106"],["四川成渝","sh601107"],["中国国航","sh601111"],["华鼎股份","sh601113"],["三江购物","sh601116"],["中国化学","sh601117"],
["海南橡胶","sh601118"],["四方股份","sh601126"],["博威合金","sh601137"],["深圳燃气","sh601139"],["重庆水务","sh601158"],["兴业银行","sh601166"],["西部矿业","sh601168"],
["北京银行","sh601169"],["杭齿前进","sh601177"],["中国西电","sh601179"],["中国铁建","sh601186"],["龙江交通","sh601188"],["东兴证券","sh601198"],["江南水务","sh601199"],
["东材科技","sh601208"],["国泰君安","sh601211"],["内蒙君正","sh601216"],["吉鑫科技","sh601218"],["林洋电子","sh601222"],["陕西煤业","sh601225"],["华电重工","sh601226"],
["环旭电子","sh601231"],["桐昆股份","sh601233"],["广汽集团","sh601238"],["庞大集团","sh601258"],["*ST二重","sh601268"],["农业银行","sh601288"],["中国北车","sh601299"],
["骆驼股份","sh601311"],["江南嘉捷","sh601313"],["中国平安","sh601318"],["交通银行","sh601328"],["广深铁路","sh601333"],["新华保险","sh601336"],["百隆东方","sh601339"],
["绿城水务","sh601368"],["陕鼓动力","sh601369"],["兴业证券","sh601377"],["怡球资源","sh601388"],["中国中铁","sh601390"],["工商银行","sh601398"],["东风股份","sh601515"],
["吉林高速","sh601518"],["大智慧","sh601519"],["东吴证券","sh601555"],["华锐风电","sh601558"],["九牧王","sh601566"],["三星电气","sh601567"],["会稽山","sh601579"],
["北辰实业","sh601588"],["鹿港科技","sh601599"],["中国铝业","sh601600"],["中国太保","sh601601"],["上海医药","sh601607"],["中信重工","sh601608"],["广电电气","sh601616"],
["中国中冶","sh601618"],["中国人寿","sh601628"],["长城汽车","sh601633"],["旗滨集团","sh601636"],["平煤股份","sh601666"],["中国建筑","sh601668"],["中国电建","sh601669"],
["明泰铝业","sh601677"],["滨化股份","sh601678"],["华泰证券","sh601688"],["拓普集团","sh601689"],["潞安环能","sh601699"],["风范股份","sh601700"],["郑煤机","sh601717"],
["际华集团","sh601718"],["上海电气","sh601727"],["中国中车","sh601766"],["力帆股份","sh601777"],["光大证券","sh601788"],["宁波建工","sh601789"],["蓝科高新","sh601798"],
["星宇股份","sh601799"],["中国交建","sh601800"],["皖新传媒","sh601801"],["中海油服","sh601808"],["光大银行","sh601818"],["中国石油","sh601857"],["中海集运","sh601866"],
["招商轮船","sh601872"],["正泰电器","sh601877"],["大连港","sh601880"],["江河创建","sh601886"],["中国国旅","sh601888"],["亚星锚链","sh601890"],["中煤能源","sh601898"],
["紫金矿业","sh601899"],["方正证券","sh601901"],["京运通","sh601908"],["国投新集","sh601918"],["中国远洋","sh601919"],["凤凰传媒","sh601928"],["吉视传媒","sh601929"],
["永辉超市","sh601933"],["建设银行","sh601939"],["金钼股份","sh601958"],["中国汽研","sh601965"],["宝钢包装","sh601968"],["海南矿业","sh601969"],["中国核电","sh601985"],
["中国银行","sh601988"],["中国重工","sh601989"],["大唐发电","sh601991"],["金隅股份","sh601992"],["丰林集团","sh601996"],["中信银行","sh601998"],["出版传媒","sh601999"],
["人民网","sh603000"],["奥康国际","sh603001"],["宏昌电子","sh603002"],["龙宇燃油","sh603003"],["晶方科技","sh603005"],["联明股份","sh603006"],["喜临门","sh603008"],
["北特科技","sh603009"],["万盛股份","sh603010"],["合锻股份","sh603011"],["创力集团","sh603012"],["弘讯科技","sh603015"],["园区设计","sh603017"],["设计股份","sh603018"],
["中科曙光","sh603019"],["爱普股份","sh603020"],["山东华鹏","sh603021"],["新通联","sh603022"],["威帝股份","sh603023"],["大豪科技","sh603025"],["石大胜华","sh603026"],
["全筑股份","sh603030"],["音飞储存","sh603066"],["和邦生物","sh603077"],["天成自控","sh603085"],["宁波精达","sh603088"],["长白山","sh603099"],["川仪股份","sh603100"],
["润达医疗","sh603108"],["康尼机电","sh603111"],["红蜻蜓","sh603116"],["万林股份","sh603117"],["共进股份","sh603118"],["翠微股份","sh603123"],["中材节能","sh603126"],
["华贸物流","sh603128"],["腾龙股份","sh603158"],["福达股份","sh603166"],["渤海轮渡","sh603167"],["莎普爱思","sh603168"],["兰石重装","sh603169"],["亚邦股份","sh603188"],
["迎驾贡酒","sh603198"],["九华旅游","sh603199"],["济民制药","sh603222"],["恒通股份","sh603223"],["雪峰科技","sh603227"],["松发股份","sh603268"],["海天味业","sh603288"],
["井神股份","sh603299"],["华铁科技","sh603300"],["华懋科技","sh603306"],["应流股份","sh603308"],["维力医疗","sh603309"],["金海环境","sh603311"],["福鞍股份","sh603315"],
["派思股份","sh603318"],["依顿电子","sh603328"],["明星电缆","sh603333"],["浙江鼎力","sh603338"],["莱克电气","sh603355"],["日出东方","sh603366"],["柳州医药","sh603368"],
["今世缘","sh603369"],["邦宝益智","sh603398"],["新华龙","sh603399"],["九洲药业","sh603456"],["思维列控","sh603508"],["维格娜丝","sh603518"],["立霸股份","sh603519"],
["贵人鸟","sh603555"],["健盛集团","sh603558"],["普莱柯","sh603566"],["珍宝岛","sh603567"],["伟明环保","sh603568"],["高能环境","sh603588"],["口子窖","sh603589"],
["引力传媒","sh603598"],["广信股份","sh603599"],["永艺股份","sh603600"],["再升科技","sh603601"],["东方电缆","sh603606"],["禾丰牧业","sh603609"],["诺力股份","sh603611"],
["韩建河山","sh603616"],["杭电股份","sh603618"],["南威软件","sh603636"],["灵康药业","sh603669"],["火炬电子","sh603678"],["龙马环卫","sh603686"],["石英股份","sh603688"],
["安记食品","sh603696"],["航天工程","sh603698"],["纽威股份","sh603699"],["盛洋科技","sh603703"],["海利生物","sh603718"],["龙韵股份","sh603729"],["隆鑫通用","sh603766"],
["乾景园林","sh603778"],["宁波高发","sh603788"],["星光农机","sh603789"],["华友钴业","sh603799"],["道森股份","sh603800"],["福斯特","sh603806"],["歌力思","sh603808"],
["曲美股份","sh603818"],["柯利达","sh603828"],["四通股份","sh603838"],["桃李面包","sh603866"],["北部湾旅","sh603869"],["老百姓","sh603883"],["吉祥航空","sh603885"],
["新澳股份","sh603889"],["好莱客","sh603898"],["晨光文具","sh603899"],["永创智能","sh603901"],["金桥信息","sh603918"],["博敏电子","sh603936"],["益丰药房","sh603939"],
["醋化股份","sh603968"],["银龙股份","sh603969"],["金诚信","sh603979"],["中电电机","sh603988"],["艾华集团","sh603989"],["洛阳钼业","sh603993"],["中新科技","sh603996"],
["继峰股份","sh603997"],["方盛制药","sh603998"],["读者传媒","sh603999"],["仪电B股","sh900901"],["市北B股","sh900902"],["大众B股","sh900903"],["神奇B股","sh900904"],
["老凤祥B","sh900905"],["中毅达B","sh900906"],["鼎立B股","sh900907"],["氯碱B股","sh900908"],["双钱B股","sh900909"],["海立B股","sh900910"],["金桥B股","sh900911"],
["外高B股","sh900912"],["国新B股","sh900913"],["锦投B股","sh900914"],["中路B股","sh900915"],["金山B股","sh900916"],["海欣B股","sh900917"],["耀皮B股","sh900918"],
["绿庭B股","sh900919"],["上柴B股","sh900920"],["丹科B股","sh900921"],["三毛B股","sh900922"],["百联B股","sh900923"],["上工B股","sh900924"],["机电B股","sh900925"],
["宝信B","sh900926"],["物贸B股","sh900927"],["自仪B股","sh900928"],["锦旅B股","sh900929"],["沪普天B","sh900930"],["PT水仙B","sh900931"],["陆家B股","sh900932"],
["华新B股","sh900933"],["锦江B股","sh900934"],["阳晨B股","sh900935"],["鄂资B股","sh900936"],["华电B股","sh900937"],["天海B","sh900938"],["汇丽B","sh900939"],
["大名城B","sh900940"],["东信B股","sh900941"],["黄山B股","sh900942"],["开开B股","sh900943"],["海航B股","sh900945"],["天雁B股","sh900946"],["振华B股","sh900947"],
["伊泰B股","sh900948"],["东电B股","sh900949"],["新城B股","sh900950"],["大化B股","sh900951"],["锦港B股","sh900952"],["凯马B","sh900953"],["九龙山B","sh900955"],
["东贝B股","sh900956"],["凌云B股","sh900957"]]

MainUrl = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/#code#.phtml"

class Handler(BaseHandler):
    crawl_config = {}
    
    @every(minutes = 24 * 60)
    def on_start(self):
        for pos in xrange(0,len(stocklist)) :
            url = MainUrl.replace("#code#",str(stocklist[pos][1]))
            self.crawl(url, callback=self.index_page, save={"code": pos })

    @config(age = 24 * 60 * 60)
    def index_page(self, response):
        pos= response.save["code"]
        for each in response.doc('ul > a').items():
            self.crawl(each.attr.href, callback=self.detail_page, save={"code" : pos})
        for nxt in response.doc('.tagmain div > a').items():
            if nxt.text() == u"下一页":
                self.crawl(nxt.attr.href, callback=self.index_page, save={"code" : pos} )
    
 
    @config(priority=2)
    def detail_page(self, response):
        maintext = ""
        if response.doc('.article_16 > p').text() != u"" :
            maintext = response.doc('.article_16 > p').text()
        elif response.doc('.BSHARE_POP > p').text() != u"" :
            maintext = response.doc('.BSHARE_POP > p').text()
            
        source = ""
        if response.doc('.time-source a').text() != u"" :
            source = response.doc('.time-source a').text()
        elif response.doc('#media_name').text() != u"" :
            source = response.doc('#media_name').text()
        
        time = ""
        if response.doc('.time-source').text() != u"" :
            time = response.doc('.time-source').text()
        elif response.doc('#pub_date').text() != u"" :
            time = response.doc('#pub_date').text()
        
        pos= response.save["code"]
        
        if maintext != u"":
            return {
                "code": stocklist[pos][1],
                "stockname": stocklist[pos][0],
                "url": response.url,
                "title": response.doc('#artibodyTitle').text(),
                "source": source,
                "time": time.replace(source,""),
                "Maintext": maintext,
            }
    
