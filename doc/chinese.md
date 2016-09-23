# zh-ud-train_6
> 就算 數論 的 應用 被 找到 了 , 也 不會 有 人 會 因 此 罷黜 這 一 數學 的 皇后 .

<!--tag=
就算/ADP 數論/NOUN 的/PART 應用/NOUN 被/VERB 找到/VERB 了/X ,/PUNCT 也/ADV 不會/AUX 有/VERB 人/NOUN 會/AUX 因/ADP 此/PRON 罷黜/VERB 這/DET 一/NUM 數學/NOUN 的/PART 皇后/NOUN ./PUNCT
-->

<!--parse=
case(就算/0, 找到/5)    det(數論/1, 應用/3)      case:dec(的/2, 數論/1)   nsubjpass(應用/3, 找到/5)
auxpass(被/4, 找到/5)  ccomp(找到/5, 有/10)    discourse(了/6, 找到/5)  punct(,/7, 有/10)
mark(也/8, 有/10)     aux(不會/9, 有/10)      root(有/10, ROOT/-1)   nsubj(人/11, 罷黜/15)
aux(會/12, 罷黜/15)    case(因/13, 此/14)     nmod(此/14, 罷黜/15)     ccomp(罷黜/15, 有/10)
det(這/16, 一/17)     nummod(一/17, 皇后/20)  det(數學/18, 皇后/20)     case:dec(的/19, 數學/18)
dobj(皇后/20, 罷黜/15)  punct(./21, 有/10)
-->

	就算 ?a 被 找到 了	[找到-ccomp]
		?a: 數論 的 應用	[應用-nsubjpass]
	就算 ?a , 也 不會 有 ?b	[有-root]
		?a: SOMETHING := 數論 的 應用 被 找到 了	[找到-ccomp]
		?b: SOMETHING := 人 會 因 此 罷黜 這 一 數學 的 皇后	[罷黜-ccomp]
	?a 會 因 ?b 罷黜 ?c	[罷黜-ccomp]
		?a: 人	[人-nsubj]
		?b: 此	[此-nmod]
		?c: 這 一 數學 的 皇后	[皇后-dobj]

# zh-ud-train_9
> 我們 只 希望 , 藉著 這 個 歷史 上 真實 人物 的 一 生 , 利用 一些 稗官野史 的 片段 資料 , 再 加上 一些 善意 改編 的 部分 情節 , 而 能 帶給 觀眾 一些 啟示 . 」

<!--tag=
tags: 我們/PRON 只/ADV 希望/VERB ,/PUNCT 藉著/ADP 這/DET 個/NOUN 歷史/NOUN 上/ADP 真實/ADJ 人物/NOUN 的/PART 一/NUM 生/NOUN ,/PUNCT 利用/VERB 一些/ADJ 稗官野史/NOUN 的/PART 片段/NOUN 資料/NOUN ,/PUNCT 再/ADV 加上/VERB 一些/ADJ 善意/NOUN 改編/VERB 的/PART 部分/NOUN 情節/NOUN ,/PUNCT 而/ADV 能/AUX 帶給/VERB 觀眾/NOUN 一些/ADJ 啟示/NOUN ./PUNCT 」/PUNCT
-->

<!--parse=
nsubj(我們/0, 希望/2)   advmod(只/1, 希望/2)     root(希望/2, ROOT/-1)      punct(,/3, 希望/2)
case(藉著/4, 生/13)    det(這/5, 個/6)         nmod(個/6, 歷史/7)          nmod(歷史/7, 生/13)
acl(上/8, 歷史/7)      amod(真實/9, 人物/10)     det(人物/10, 生/13)         case:dec(的/11, 人物/10)
nummod(一/12, 生/13)  nmod(生/13, 帶給/33)     punct(,/14, 帶給/33)       acl(利用/15, 帶給/33)
amod(一些/16, 資料/20)  det(稗官野史/17, 資料/20)   case:dec(的/18, 稗官野史/17)  nmod(片段/19, 資料/20)
dobj(資料/20, 利用/15)  punct(,/21, 帶給/33)    advmod(再/22, 加上/23)      acl(加上/23, 帶給/33)
amod(一些/24, 情節/29)  advmod(善意/25, 改編/26)  acl:relcl(改編/26, 情節/29)  acl:relcl(的/27, 改編/26)
nmod(部分/28, 情節/29)  dobj(情節/29, 加上/23)    punct(,/30, 帶給/33)       mark(而/31, 帶給/33)
aux(能/32, 帶給/33)    xcomp(帶給/33, 希望/2)    iobj(觀眾/34, 帶給/33)       amod(一些/35, 啟示/36)
dobj(啟示/36, 帶給/33)  punct(./37, 希望/2)     punct(」/38, 希望/2)
-->

	?a 只 希望 , 藉著 ?b , 而 能 帶給 ?c ?d	[希望-root]
		?a: 我們	[我們-nsubj]
		?b: 這 個 歷史 真實 人物 的 一 生	[生-nmod]
		?c: 觀眾	[觀眾-iobj]
		?d: 一些 啟示	[啟示-dobj]

# zh-ud-train_10
> 當時 外界 傳聞 樊 日行 是 在 中視 主管 授意 下 裝病 , 樊 日行 否認 : 「 人 都是 吃 五 穀 雜糧 長大 , 本來 就 會 生病 ; 而且 裝病 萬一 被 拆穿 了 , 豈 不是 無法 對 廣大 的 觀眾 交代 ?

<!--tag=
tags: 當時/NOUN 外界/NOUN 傳聞/VERB 樊/PROPN 日行/PROPN 是/VERB 在/ADP 中視/PROPN 主管/NOUN 授意/NOUN 下/ADP 裝病/VERB ,/PUNCT 樊/PROPN 日行/PROPN 否認/VERB :/PUNCT 「/PUNCT 人/NOUN 都是/VERB 吃/VERB 五/NUM 穀/NOUN 雜糧/NOUN 長大/VERB ,/PUNCT 本來/ADV 就/ADV 會/AUX 生病/VERB ;/PUNCT 而且/ADV 裝病/VERB 萬一/ADV 被/VERB 拆穿/VERB 了/X ,/PUNCT 豈/ADV 不是/VERB 無法/VERB 對/ADP 廣大/ADJ 的/PART 觀眾/NOUN 交代/VERB ?/PUNCT
-->

<!--parse=
nmod:tmod(當時/0, 傳聞/2)    nmod(外界/1, 傳聞/2)      dep(傳聞/2, 否認/15)      nmod(樊/3, 日行/4)
nsubj(日行/4, 是/5)         ccomp(是/5, 傳聞/2)      case(在/6, 授意/9)       nmod(中視/7, 授意/9)
nmod(主管/8, 授意/9)         nmod(授意/9, 裝病/11)     acl(下/10, 授意/9)       xcomp(裝病/11, 是/5)
punct(,/12, 否認/15)       nmod(樊/13, 日行/14)     nsubj(日行/14, 否認/15)   root(否認/15, ROOT/-1)
punct(:/16, 否認/15)       punct(「/17, 不是/39)    nsubj(人/18, 生病/29)    acl(都是/19, 生病/29)
acl(吃/20, 長大/24)         nummod(五/21, 穀/22)    nmod(穀/22, 雜糧/23)     dobj(雜糧/23, 吃/20)
xcomp(長大/24, 都是/19)      punct(,/25, 生病/29)    advmod(本來/26, 生病/29)  mark(就/27, 生病/29)
aux(會/28, 生病/29)         dep(生病/29, 不是/39)     punct(;/30, 不是/39)    mark(而且/31, 不是/39)
csubjpass(裝病/32, 拆穿/35)  advmod(萬一/33, 拆穿/35)  auxpass(被/34, 拆穿/35)  dep(拆穿/35, 不是/39)
discourse(了/36, 拆穿/35)   punct(,/37, 不是/39)    advmod(豈/38, 不是/39)   ccomp(不是/39, 否認/15)
xcomp(無法/40, 不是/39)      case(對/41, 觀眾/44)     amod(廣大/42, 觀眾/44)    acl:relcl(的/43, 廣大/42)
nmod(觀眾/44, 交代/45)       xcomp(交代/45, 無法/40)   punct(?/46, 不是/39)
-->

	?a 是 在 ?b 裝病	[是-ccomp]
		?a: 樊 日行	[日行-nsubj]
		?b: 中視 主管 授意	[授意-nmod]
	?a 否認 ?b	[否認-root]
		?a: 樊 日行	[日行-nsubj]
		?b: SOMETHING := 豈 不是 無法 對 廣大 觀眾 交代	[不是-ccomp]
	?a 豈 不是 無法 對 ?b 交代	[不是-ccomp]
		?a: 樊 日行	[日行-nsubj]
		?b: 廣大 觀眾	[觀眾-nmod]

# zh-ud-train_44
> 它 還 與 五氧化二氮 催化 臭氧 分解 的 反應 有關 , 這 對 臭氧 層 會 造成 破壞 , 因 此 引起 了 人們 的 興趣 .

<!--tag=
tags: 它/PRON 還/ADV 與/ADP 五氧化二氮/NOUN 催化/VERB 臭氧/NOUN 分解/VERB 的/PART 反應/NOUN 有關/ADJ ,/PUNCT 這/PRON 對/ADP 臭氧/NOUN 層/PART 會/AUX 造成/VERB 破壞/NOUN ,/PUNCT 因/ADP 此/PRON 引起/VERB 了/PART 人們/NOUN 的/PART 興趣/NOUN ./PUNCT
-->

<!--parse=
nsubj(它/0, 有關/9)       mark(還/1, 有關/9)         case(與/2, 反應/8)           nsubj(五氧化二氮/3, 催化/4)
acl:relcl(催化/4, 反應/8)  nsubj(臭氧/5, 分解/6)       ccomp(分解/6, 催化/4)         acl:relcl(的/7, 催化/4)
nmod(反應/8, 有關/9)       dep(有關/9, 引起/21)        punct(,/10, 引起/21)        nsubj(這/11, 引起/21)
case(對/12, 層/14)       case:suff(臭氧/13, 層/14)  nmod(層/14, 造成/16)         aux(會/15, 造成/16)
acl(造成/16, 引起/21)      dobj(破壞/17, 造成/16)      punct(,/18, 引起/21)        case(因/19, 此/20)
nmod(此/20, 引起/21)      root(引起/21, ROOT/-1)    case:aspect(了/22, 引起/21)  det(人們/23, 興趣/25)
case:dec(的/24, 人們/23)  dobj(興趣/25, 引起/21)      punct(./26, 引起/21)
-->

	?a 催化 ?b ?c	[催化-acl:relcl]
		?a: 五氧化二氮	[五氧化二氮-nsubj]
		?b: SOMETHING := 臭氧 分解	[分解-ccomp]
		?c: 反應	[反應-nmod]
	?a 分解	[分解-ccomp]
		?a: 臭氧	[臭氧-nsubj]
