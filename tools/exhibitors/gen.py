import html, json, sys, os, urllib.parse
OUT = sys.argv[1]
SITE = 'https://www.rmafcinvestmentsummit2026.org'
MAIL = 'summit@rmafcinvestmentsummit2026.org'
E = html.escape

COMPANIES = [
 dict(slug='alfan-gas', name='Alfan Gas Nigeria Limited', zh='阿尔凡天然气尼日利亚有限公司',
  kicker=('Midstream gas · Gas processing', '中游天然气 · 天然气处理'),
  lede=('An established Delta State LPG supplier, in business since 2017, now developing a natural gas processing plant to produce its own LPG, propane, butane, condensate and lean gas for Nigeria\'s domestic and industrial markets.',
        '一家自2017年起经营的三角洲州液化石油气供应商，现正开发天然气处理厂，自主生产液化石油气、丙烷、丁烷、凝析油和贫气，供应尼日利亚国内及工业市场。'),
  facts=[('Project','项目','Natural gas processing plant (NGPP)','天然气处理厂（NGPP）'),
         ('Raw gas capacity','原料气处理能力','50 MMSCFD (large plant) to 100+ MMSCFD (industrial scale)','5,000万立方英尺/日（大型）至1亿立方英尺/日以上（工业级）'),
         ('Products','产品','LPG, commercial propane, butane, white and brown condensate, lean gas; ethane where economic','液化石油气、商用丙烷、丁烷、白/棕凝析油、贫气；经济可行时回收乙烷'),
         ('Stage','阶段','Concept: plant sizing and configuration under study','概念阶段：工厂规模与配置研究中'),
         ('Current business','现有业务','Bulk sale, distribution and supply of LPG to gas retail plants, manufacturers and power generators','向燃气零售站、制造企业及发电企业批量销售、分销和供应液化石油气'),
         ('Established','成立','2017; incorporated as a limited company in 2019 (RC 1551803)','2017年；2019年注册为有限公司（注册号1551803）'),
         ('Chief executive','首席执行官','Okogwu Emmanuel','Okogwu Emmanuel'),
         ('Head office','总部','Obiaruku, Delta State','三角洲州奥比亚鲁库')],
  about=[('Alfan Gas Nigeria is a privately owned indigenous company. It started in 2017 as Alfan Gas Nigeria Enterprises and became a limited company in 2019 as its LPG sales and distribution business grew. It supplies LPG in bulk to gas retail plants, manufacturers and power generators, and holds 2026 offtake permits for LPG and propane. The processing plant moves the company upstream of its own supply.',
          'Alfan天然气尼日利亚有限公司是一家私营本土企业，2017年以Alfan Gas Nigeria Enterprises名义创立，随着液化石油气销售与分销业务的增长，于2019年改制为有限公司。公司向燃气零售站、制造企业和发电企业批量供应液化石油气，并持有2026年液化石油气及丙烷提货许可。天然气处理厂项目将使公司向供应链上游延伸。'),
         ('The plant is designed to separate raw natural gas or associated gas into products with clear Nigerian demand: LPG for homes and industry, propane for industrial heating, petrochemical feedstock and power, butane for LPG blending, condensates for refineries and petrochemicals, and methane-rich lean gas for power, CNG, LNG and industrial supply.',
          '该处理厂旨在将原料天然气或伴生气分离为尼日利亚市场需求明确的产品：供家庭和工业使用的液化石油气，用于工业供热、石化原料和发电的丙烷，用于液化石油气调和的丁烷，供炼油和石化使用的凝析油，以及用于发电、压缩天然气、液化天然气和工业供气的富甲烷贫气。'),
         ('The core process train covers inlet separation, gas sweetening, dehydration, refrigeration or cryogenic NGL recovery, fractionation, condensate stabilisation, compression, LPG storage, loading facilities and safety systems.',
          '核心工艺包括入口分离、天然气脱硫、脱水、制冷或深冷天然气凝液回收、分馏、凝析油稳定、压缩、液化石油气储存、装车设施及安全系统。')],
  seeking=[('Equity and project finance for the processing plant','处理厂的股权投资与项目融资'),
           ('EPC contractors with gas-processing experience','具有天然气处理经验的EPC承包商'),
           ('Suppliers of separation, sweetening, NGL recovery, fractionation and compression packages','分离、脱硫、凝液回收、分馏及压缩成套设备供应商'),
           ('Offtakers for LPG, propane and condensate','液化石油气、丙烷及凝析油承购方')],
  docs=[('Company profile','公司简介'),('Corporate registration (CAC)','公司注册文件（CAC）'),('2026 tax clearance certificate','2026年完税证明'),('2026 LPG and propane offtake permits','2026年液化石油气及丙烷提货许可')],
  sources=[]),

 dict(slug='reditto-centrale', name='Reditto Centrale', zh='Reditto Centrale 投资促进与产业合作',
  kicker=('Downstream · Petrochemicals', '下游 · 石油化工'),
  lede=('An investment-promotion and industrial-partnership firm bringing manufacturers into Nigeria\'s downstream petrochemical sector, built on feedstock from Nigeria\'s domestic refineries.',
        '一家投资促进与产业合作机构，致力于引导制造企业进入尼日利亚下游石化行业，以尼日利亚国内炼油厂的原料为基础。'),
  facts=[('Focus','重点领域','Polymers (polypropylene, polyethylene), lubricant blending, paints and coatings, fertiliser inputs','聚合物（聚丙烯、聚乙烯）、润滑油调和、涂料、化肥原料'),
         ('Feedstock','原料','Domestic refinery output: polypropylene, polyethylene, base oils, solvents and sulfur','国内炼油厂产品：聚丙烯、聚乙烯、基础油、溶剂和硫磺'),
         ('Target sectors','目标行业','Ten, led by flexible and rigid packaging, woven sacks, plastic pipes and household products','十个行业，首批包括软包装、硬包装、编织袋、塑料管材及家居用品'),
         ('Location','区位','Lekki industrial corridor, Lagos','拉各斯莱基工业走廊'),
         ('Model','模式','Connects manufacturers with feedstock, finance, free-zone and government support','为制造企业对接原料、融资、自由区及政府支持'),
         ('Chief executive','首席执行官','Temitope Osho','Temitope Osho')],
  about=[('Nigeria now has a large domestic source of polypropylene, polyethylene, base oils, solvents and sulfur, with the Dangote Refinery and Petrochemical Complex at Ibeju-Lekki on the Lekki corridor. Reditto Centrale helps manufacturers turn that feedstock into finished goods made in Nigeria rather than exported as raw material.',
          '尼日利亚现已拥有聚丙烯、聚乙烯、基础油、溶剂和硫磺的大规模国内来源，丹格特炼油及石化综合体即位于莱基走廊的伊贝朱-莱基。Reditto Centrale 帮助制造企业将这些原料转化为尼日利亚本地制造的成品，而非以原料形式出口。'),
         ('It has mapped ten manufacturing sectors that use this output as direct raw material. The first wave is flexible packaging, rigid packaging, polypropylene woven sacks, plastic pipes and fittings, and household products. The second wave is automotive plastics, plastic compounding, lubricant blending, and paints and coatings, with sulfuric acid and fertiliser as a strategic sector. These are target sectors with indicative feedstock needs, not committed investors.',
          '公司梳理了十个以上述产品为直接原料的制造行业。首批为软包装、硬包装、聚丙烯编织袋、塑料管材管件及家居用品；第二批为汽车塑料件、塑料改性造粒、润滑油调和以及涂料，硫酸及化肥为战略性行业。以上为具有指示性原料需求的目标行业，并非已承诺的投资方。'),
         ('Reditto works in three steps: it identifies manufacturers and defines each one\'s feedstock needs; introduces them to feedstock suppliers, free-zone operators, financiers and agencies; and coordinates the parties so that site, finance and approvals line up. The Lekki corridor puts feedstock, free-zone and port infrastructure in one place.',
          'Reditto的工作分三步：识别制造企业并明确其原料需求；为其对接原料供应商、自由区运营商、融资方及政府机构；协调各方，使选址、融资与审批同步推进。莱基走廊将原料、自由区和港口基础设施集中于一地。')],
  seeking=[('Chinese manufacturers of plastics, packaging, lubricants, coatings and fertilisers','塑料、包装、润滑油、涂料及化肥领域的中国制造企业'),
           ('Financiers for downstream industrial projects','下游工业项目的融资方'),
           ('Free-zone operators and industrial-park developers','自由区运营商及产业园开发商'),
           ('Equipment suppliers for compounding and blending plants','改性造粒及调和工厂的设备供应商')],
  docs=[('Partner brief','合作伙伴简介')],
  sources=[]),

 dict(slug='hilltop-global', name="Hilltop Global Oil and Gas Solutions Int'l Ltd", zh='希尔托普环球油气解决方案国际有限公司',
  own_photos=True,
  kicker=('Upstream · Marginal field', '上游 · 边际油田'),
  lede=('An indigenous engineering and oilfield-services company that now holds 100% of the Alaoma heavy-oil field in Imo State, and is seeking investment to re-enter its existing wells and drill new ones.',
        '一家尼日利亚本土工程及油田服务公司，现100%持有伊莫州Alaoma重油油田，正在寻求投资以重新进入现有油井并钻探新井。'),
  facts=[('Asset','资产','Alaoma marginal field, OML 53 South','Alaoma边际油田，OML 53南部'),
         ('Location','位置','Umuneke Ngo community, Ngor Okpala LGA, Imo State (onshore Niger Delta)','伊莫州Ngor Okpala地方政府区Umuneke Ngo社区（尼日尔三角洲陆上）'),
         ('Licence','许可证','Petroleum Prospecting Licence (PPL) 224, 100% held','石油勘探许可证（PPL）224，100%持有'),
         ('Licence granted','授予日期','28 June 2022, by NUPRC','2022年6月28日，由NUPRC授予'),
         ('Licence area','许可区面积','34.06 km²','34.06平方公里'),
         ('Discovery','发现','Discovered by Chevron in 1996; existing wells on the field','1996年由雪佛龙发现；油田上已有油井'),
         ('Crude','原油','Heavy, biodegraded oil, 8–18° API','重质生物降解原油，API度8–18°'),
         ('Status','现状','Land and site preparation complete; drilling rig selected; NUPRC approval for well re-entry in progress','土地及场地准备已完成；钻机已选定；油井重入的NUPRC审批正在办理'),
         ('Group CEO','集团首席执行官','Dr Charles Osazuwa','Charles Osazuwa博士'),
         ('Offices','办公地点','Benin City (head office), Abuja, Houston','贝宁城（总部）、阿布贾、休斯敦')],
  about=[('Hilltop holds Petroleum Prospecting Licence 224 over the Alaoma marginal field, awarded by the Nigerian Upstream Petroleum Regulatory Commission (NUPRC) on 28 June 2022 and registered as 100% held by Hilltop. The field lies in the south-east of OML 53, onshore Imo State. Chevron discovered it in 1996, and fluid typing shows heavy, biodegraded oil of 8 to 18° API with large resource volumes. Jisike, in the north-west of the same block, is already in production.',
          'Hilltop持有Alaoma边际油田的第224号石油勘探许可证，该许可证由尼日利亚上游石油监管委员会（NUPRC）于2022年6月28日授予，登记为Hilltop 100%持有。油田位于伊莫州陆上OML 53区块东南部，1996年由雪佛龙发现。流体分析显示其为API度8至18°的重质生物降解原油，资源量较大。同一区块西北部的Jisike油田已投入生产。'),
         ('Groundwork on the field is done. Survey and mapping of the operating area, engagement with landowners across the host communities, land acquisition for well re-entry and the facilities layout, and site clearing are all complete. A drilling rig has been inspected and selected, and Hilltop is obtaining NUPRC approval to re-enter the existing Chevron wells and to drill new wells.',
          '油田前期工作已经完成：作业区勘测与测绘、与各东道社区土地所有者的沟通、油井重入及设施布局所需土地的征用以及场地清理均已完工。公司已完成钻机考察与选定，并正在申请NUPRC批准，以重新进入雪佛龙原有油井并钻探新井。'),
         ('Hilltop started as an engineering, procurement and construction (EPC) and oilfield-services company and still runs that business. Its work includes supplying pressure control valves for well operations to NNPC Exploration & Production Ltd, bill-of-materials and cost control for a 120 MMSCFD gas compression and dehydration plant on OML 111, and engineering support for the design of a 29-tank LPG storage terminal at Ovade-Ogharefe. It runs a quality management system aligned with ISO 9001:2015.',
          'Hilltop最初是一家工程、采购与施工（EPC）及油田服务公司，目前仍经营该业务。其业绩包括：为尼日利亚国家石油公司勘探与生产有限公司（NEPL）供应油井作业用压力控制阀；为OML 111区块一座日处理1.2亿标准立方英尺的天然气压缩脱水厂提供物料清单及成本控制服务；为Ovade-Ogharefe一座含29个储罐的液化石油气储运站的设计提供工程支持。公司按照ISO 9001:2015标准运行质量管理体系。')],
  seeking=[('Equity or development finance to re-enter the existing wells and drill new ones','用于重入现有油井及钻探新井的股权投资或开发融资'),
           ('Technical partners with heavy-oil production experience','具有重油开采经验的技术合作伙伴'),
           ('Drilling, well-services and early-production-facility contractors','钻井、井下作业及早期生产设施承包商'),
           ('Offtakers and refiners for heavy crude','重质原油的承购方及炼厂')],
  docs=[('Company profile, with field survey and rig inspection photographs','公司简介（附油田勘测及钻机考察照片）'),
        ('NUPRC licence record for PPL 224','PPL 224的NUPRC许可证登记记录')],
  sources=[('NUPRC concession situation, 1 April 2026','https://www.nuprc.gov.ng/wp-content/uploads/2026/04/NUPRC-Concession-Situation-@-1st-April-2026-V.1.pdf')]),

 dict(slug='boj-energy', name='BOJ Energy Ltd', zh='BOJ能源有限公司',
  kicker=('Upstream · Producing assets', '上游 · 在产资产'),
  lede=('An Abuja-based Nigerian oil company focused on indigenous acquisition of producing assets, with an interest in the Ogedeh marginal field.',
        '一家总部位于阿布贾的尼日利亚石油公司，专注于本土企业收购在产资产，并拥有Ogedeh边际油田的权益。'),
  facts=[('Focus','重点领域','Indigenous acquisition of producing oil and gas assets','本土企业收购在产油气资产'),
         ('Asset','资产','Ogedeh marginal field (block from OML 90)','Ogedeh边际油田（由OML 90划出的区块）'),
         ('Chairman','董事长','Ajayi Alfred Agboola','Ajayi Alfred Agboola'),
         ('Head office','总部','16 Abubakar Koko Crescent, Asokoro, Abuja','阿布贾阿索科罗区Abubakar Koko新月街16号')],
  about=[('BOJ Energy is part of the new generation of Nigerian-owned upstream companies taking over onshore and shallow-water assets as international oil companies divest. Its strategy is to acquire assets that are already producing, or close to production, and grow output under Nigerian ownership.',
          'BOJ能源是新一代尼日利亚本土上游公司之一，随着国际石油公司剥离资产，这些公司正在接手陆上及浅水资产。其战略是收购已投产或即将投产的资产，在尼日利亚人所有权下提高产量。'),
         ('The company holds an interest in the Ogedeh marginal field, a block carved out of OML 90.',
          '公司持有Ogedeh边际油田的权益，该区块由OML 90划出。')],
  seeking=[('Acquisition finance for producing assets','在产资产的收购融资'),
           ('Development capital for the Ogedeh field','Ogedeh油田的开发资金'),
           ('Technical and operating partners','技术及运营合作伙伴'),
           ('Crude offtakers and traders','原油承购方及贸易商')],
  docs=[],
  sources=[]),

 dict(slug='ace-energy', name='Ace Energy Group', zh='Ace能源集团',
  kicker=('Gas · LNG, upstream and refining', '天然气 · 液化天然气、上游与炼化'),
  lede=('A Lagos-based energy group developing the 3 MTPA Ace FLNG and 235 MW power barge offshore Escravos, near-term oil production in the Niger Delta, and a 100,000 bopd refinery at Burutu.',
        '一家总部位于拉各斯的能源集团，正在开发埃斯克拉沃斯近海300万吨/年Ace浮式液化天然气（FLNG）及235兆瓦发电驳船、尼日尔三角洲近期原油生产项目，以及布鲁图日加工10万桶的炼油厂。'),
  facts=[('Flagship project','旗舰项目','3 MTPA Ace FLNG and 235 MW power barge, about 10 km offshore Escravos','埃斯克拉沃斯近海约10公里处的300万吨/年Ace FLNG及235兆瓦发电驳船'),
         ('Gas resource','天然气资源','Over 7 Tcf of non-associated and associated gas, four concessions within 100 km','逾7万亿立方英尺非伴生气及伴生气，100公里范围内四个区块'),
         ('FLNG output','FLNG产出','3 MTPA LNG · 25,000 bopd condensate · 700 t/day LPG · 300 t/day propane, from 550 MMSCFD wet gas','液化天然气300万吨/年 · 凝析油2.5万桶/日 · 液化石油气700吨/日 · 丙烷300吨/日（处理湿气5.5亿立方英尺/日）'),
         ('FLNG investment','FLNG投资额','About US$5.5 billion, integrated upstream and midstream','约55亿美元，上中游一体化'),
         ('FLNG stage','FLNG阶段','FEED with Wison New Energies; first gas targeted Q2 2030','由惠生新能源开展FEED；目标2030年第二季度首气'),
         ('Oil production','原油生产','Osuopele field (OML 46), Delta State: first oil by barge to Forcados targeted 9–12 months from sanction','三角洲州Osuopele油田（OML 46）：目标在投资决策后9–12个月通过驳船运往福卡多斯实现首油'),
         ('Refining','炼化','100,000 bopd full-conversion refinery at Burutu, Delta State, in development','三角洲州布鲁图日加工10万桶全转化炼油厂，开发中'),
         ('Head office','总部','6A Lapaz Place, Victoria Island, Lagos','拉各斯维多利亚岛Lapaz Place 6A号'),
         ('Contact','联系人','Christopher Nwokolo','Christopher Nwokolo')],
  about=[('Ace Energy Group works across the oil and gas chain through separate platforms for gas and FLNG, upstream oil, and refining and trading. Its Nigerian projects cover gas export, near-term crude production and domestic refining.',
          'Ace能源集团通过天然气及FLNG、上游原油、炼化及贸易等独立平台覆盖油气全产业链。其在尼日利亚的项目涵盖天然气出口、近期原油生产和本土炼油。'),
         ('The Ace FLNG and power barge are collocated to process wet gas from several sources around the Escravos and Forcados hub. The barge powers Ace\'s gas assets and nearby processing facilities; the FLNG produces LNG for export together with condensate, LPG and propane. Chinese contractor Wison New Energies completed pre-FEED in early 2024 and signed the FEED contract in December 2024. Liquefaction uses Chart Industries\' IPSMR technology, and Siemens Energy is lined up for power and compression. According to the company, NNPC has committed feedstock gas.',
          'Ace FLNG与发电驳船同址布置，处理埃斯克拉沃斯和福卡多斯枢纽周边多个来源的湿气。发电驳船为Ace的天然气资产及附近处理设施供电；FLNG生产出口液化天然气，同时产出凝析油、液化石油气和丙烷。中国承包商惠生新能源（Wison New Energies）于2024年初完成预可研设计（pre-FEED），并于2024年12月签署FEED合同。液化工艺采用Chart公司的IPSMR技术，西门子能源负责发电和压缩系统。据公司介绍，NNPC已承诺提供原料气。'),
         ('In upstream oil, Ace plans fast first oil from the Osuopele swamp field in Delta State, shipping crude by barge to Forcados and using its own FPSO as a storage and export hub. A second phase would tie in the Bita field (OML 95), the Bilabri field (OML 122) and the deepwater OPL 289. Outside Nigeria, the group holds or is pursuing acreage in Angola, Gabon and Somaliland.',
          '在上游原油方面，Ace计划通过三角洲州Osuopele沼泽油田快速实现首油，以驳船将原油运至福卡多斯，并以自有FPSO作为储存和外输枢纽。第二阶段将接入Bita油田（OML 95）、Bilabri油田（OML 122）及深水区块OPL 289。在尼日利亚以外，集团在安哥拉、加蓬和索马里兰持有或正在争取区块。'),
         ('Ace Global Refining and Trading, the group\'s downstream arm, is developing a 100,000 bopd full-conversion refinery at Burutu in Delta State as part of nine refining, blending, petrochemical and storage projects in six countries. Its preferred contractor panel includes Wison, CNCEC, TCC and CMEC.',
          '集团下游平台Ace全球炼化与贸易公司正在三角洲州布鲁图开发一座日加工10万桶的全转化炼油厂，该项目属于其在六个国家开发的九个炼油、调和、石化及仓储项目之一。其首选承包商包括惠生、中国化学工程、TCC和中国机械设备工程（CMEC）。'),
         ('Ace has also partnered with NNPC on flare-to-value projects: barge-mounted and land-based flare-to-LNG, and flare gas to low-carbon aviation fuel.',
          'Ace还与NNPC合作开发燃除气增值项目：驳船式及陆上燃除气制液化天然气，以及燃除气制低碳航空燃料。')],
  seeking=[('Equity and project finance for the Ace FLNG (over US$1 billion)','Ace FLNG的股权投资与项目融资（逾10亿美元）'),
           ('LNG offtakers and buyers in China','中国的液化天然气承购方和买家'),
           ('Equity, debt and crude offtake for the Osuopele production hub','Osuopele生产枢纽的股权、债务融资及原油承购'),
           ('EPC, fabrication and finance partners for the Burutu refinery','布鲁图炼油厂的EPC、制造及融资合作伙伴'),
           ('Investors for flare-gas-to-LNG and aviation-fuel projects','燃除气制液化天然气及航空燃料项目的投资者')],
  docs=[('NNPC–Ace FLNG terms of reference','NNPC–Ace FLNG项目任务书'),('Ace Global Refining and Trading company profile','Ace全球炼化与贸易公司简介'),('Ace upstream portfolio (investor teaser, under NDA)','Ace上游资产组合（投资者简介，需签署保密协议）')],
  sources=[('Gas Processing & LNG: Wison New Energies and Ace Gas & FLNG sign FEED contract','https://www.gasprocessingnews.com/news/2024/12/wison-new-energies-ace-gas-flng-sign-feed-contract-for-nigeria-flng-project/'),
           ('Global Energy Monitor: Ace Gas Nigeria FLNG Terminal','https://gem.wiki/Ace_Gas_Nigeria_FLNG_Terminal')]),
]

IMAGES = {'alfan-gas': [('/assets/photo-flare-recovery.jpg', 'Gas processing modules', '天然气处理模块'), ('/assets/photo-pipeline.jpg', 'Gas pipeline', '天然气管道')], 'reditto-centrale': [('/assets/photo-lng-terminal.jpg', 'Coastal industrial and storage terminal', '沿海工业及储运码头'), ('/assets/exhibitors/industrial-site.jpg', 'Industrial site under construction', '在建工业场地')], 'hilltop-global': [('/assets/exhibitors/hilltop-alaoma-site.jpg', 'Alaoma field: cleared site', 'Alaoma油田：已清理场地'), ('/assets/exhibitors/hilltop-rig-inspection.jpg', 'Rig inspection for Alaoma', 'Alaoma钻机考察'), ('/assets/exhibitors/hilltop-wellhead.jpg', 'Existing Alaoma wellhead', 'Alaoma现有井口')], 'boj-energy': [('/assets/photo-pipeline.jpg', 'Onshore production facilities', '陆上生产设施'), ('/assets/exhibitors/upstream-crew.jpg', 'Wellsite operations', '井场作业')], 'ace-energy': [('/assets/photo-lng-flng.jpg', 'Floating LNG and export', '浮式液化天然气及外输'), ('/assets/photo-hero-fpso.jpg', 'Offshore gas processing', '海上天然气处理')]}

TPL = open(os.path.join(os.path.dirname(__file__), 'page.tpl')).read()

def li(items):
    return ''.join(f'<li data-zh="{E(z)}">{E(e)}</li>' for e, z in items)

for c in COMPANIES:
    url = f"{SITE}/{c['slug']}"
    subj = urllib.parse.quote(f"Meeting request: {c['name']}")
    body = urllib.parse.quote(f"I would like to meet {c['name']} at the RMAFC Oil & Gas Investment Summit in Beijing.\n\nName:\nOrganisation:\nCountry:\nInterest:\n")
    facts = ''.join(f'<div class="fact"><dt data-zh="{E(lz)}">{E(le)}</dt><dd data-zh="{E(vz)}">{E(ve)}</dd></div>' for le, lz, ve, vz in c['facts'])
    about = ''.join(f'<p data-zh="{E(z)}">{E(e)}</p>' for e, z in c['about'])
    docs = ('<div class="docs"><h3 class="mono" data-zh="向秘书处提交的资料">Documents on file with the secretariat</h3><ul>' + li(c['docs']) +
            '</ul><p class="small" data-zh="已注册代表可通过秘书处索取。">Available to registered delegates on request through the secretariat.</p></div>') if c['docs'] else ''
    src = ('<p class="small src"><span data-zh="公开来源：">Public sources:</span> ' + ' · '.join(f'<a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a>' for t, u in c['sources']) + '</p>') if c['sources'] else ''
    desc = c['lede'][0]
    ims = IMAGES[c['slug']]
    gallery = ''.join(f'<figure><img src="{E(u)}" alt="{E(a)}" loading="{"eager" if i==0 else "lazy"}"><figcaption data-zh="{E(z)}">{E(a)}</figcaption></figure>' for i,(u,a,z) in enumerate(ims))
    if c.get('own_photos'):
        note = ('<p class="illus" data-zh="照片由企业提供。">Photographs supplied by the company.</p>')
    else:
        note = ('<p class="illus" data-zh="示意图片。企业提供实景照片后将予以替换。">Illustrative images. They will be replaced with the company\'s own photographs once supplied.</p>')
    grid = 'grid three' if len(ims) == 3 else 'grid'
    out = (TPL.replace('{{NAME}}', E(c['name'])).replace('{{NAME_ZH}}', E(c['zh'])).replace('{{URL}}', url)
           .replace('{{DESC}}', E(desc)).replace('{{KICKER}}', E(c['kicker'][0])).replace('{{KICKER_ZH}}', E(c['kicker'][1]))
           .replace('{{LEDE}}', E(c['lede'][0])).replace('{{LEDE_ZH}}', E(c['lede'][1]))
           .replace('{{FACTS}}', facts).replace('{{ABOUT}}', about).replace('{{SEEKING}}', li(c['seeking']))
           .replace('{{DOCS}}', docs).replace('{{SOURCES}}', src)
           .replace('{{MAILTO}}', f'mailto:{MAIL}?subject={subj}&amp;body={body}')
           .replace('{{GALLERY}}', gallery).replace('{{GALLERYNOTE}}', note).replace('{{GRIDCLASS}}', grid).replace('{{OGIMG}}', SITE + ims[0][0]).replace('{{SLUG}}', c['slug']).replace('{{JSONLD}}', json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": c['name'], "description": desc, "url": url}, ensure_ascii=False)))
    open(os.path.join(OUT, c['slug'] + '.html'), 'w').write(out)
    print(c['slug'], len(out))
