import html, json, sys, os, urllib.parse
OUT = sys.argv[1]
SITE = 'https://www.rmafcinvestmentsummit2026.org'
MAIL = 'summit@rmafcinvestmentsummit2026.org'
E = html.escape

COMPANIES = [
 dict(slug='alfan-gas', name='Alfan Gas Nigeria Limited', zh='阿尔凡天然气尼日利亚有限公司',
  kicker=('Midstream gas · Gas processing', '中游天然气 · 天然气处理'),
  lede=('A Nigerian gas company developing a natural gas processing plant that turns raw and associated gas into LPG, propane, butane, condensate and lean gas for Nigeria\'s domestic and industrial markets.',
        '一家尼日利亚天然气公司，正在开发天然气处理厂，将原料气和伴生气加工为液化石油气、丙烷、丁烷、凝析油和贫气，供应尼日利亚国内及工业市场。'),
  facts=[('Project','项目','Natural gas processing plant (NGPP)','天然气处理厂（NGPP）'),
         ('Raw gas capacity','原料气处理能力','50 MMSCFD (large plant) to 100+ MMSCFD (industrial scale)','5,000万立方英尺/日（大型）至1亿立方英尺/日以上（工业级）'),
         ('Products','产品','LPG, commercial propane, butane, white and brown condensate, lean gas; ethane where economic','液化石油气、商用丙烷、丁烷、白/棕凝析油、贫气；经济可行时回收乙烷'),
         ('Stage','阶段','Concept: plant sizing and configuration under study','概念阶段：工厂规模与配置研究中'),
         ('Chief executive','首席执行官','Okogwu Emmanuel','Okogwu Emmanuel'),
         ('Headquarters','总部','Nigeria','尼日利亚')],
  about=[('The plant is designed to separate raw natural gas or associated gas into products with clear Nigerian demand: LPG for homes and industry, propane for industrial heating, petrochemical feedstock and power, butane for LPG blending, condensates for refineries and petrochemicals, and methane-rich lean gas for power, CNG, LNG and industrial supply.',
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
         ('Feedstock','原料','Domestic refinery output: polymers, base oils and solvents','国内炼油厂产品：聚合物、基础油和溶剂'),
         ('Location','区位','Lekki industrial corridor, Lagos','拉各斯莱基工业走廊'),
         ('Model','模式','Connects manufacturers with feedstock, finance, free-zone and government support','为制造企业对接原料、融资、自由区及政府支持'),
         ('Chief executive','首席执行官','Temitope Osho','Temitope Osho')],
  about=[('Nigeria now refines more of its own crude, and the refinery output opens a domestic supply of polypropylene, polyethylene, base oils and solvents. Reditto Centrale helps manufacturers turn that feedstock into local production: plastics and packaging, lubricants, paints and coatings, and fertiliser inputs.',
          '尼日利亚国内炼油能力不断提升，炼厂产品为聚丙烯、聚乙烯、基础油和溶剂提供了本地供应。Reditto Centrale 帮助制造企业将这些原料转化为本地生产：塑料与包装、润滑油、涂料以及化肥原料。'),
         ('The firm brings together the pieces a manufacturer needs to invest: feedstock supply, finance, free-zone incentives and government support, with a focus on industrial projects around the Lekki corridor in Lagos.',
          '该机构为制造企业整合投资所需的各个环节：原料供应、融资、自由区激励政策和政府支持，重点关注拉各斯莱基走廊周边的工业项目。')],
  seeking=[('Chinese manufacturers of plastics, packaging, lubricants, coatings and fertilisers','塑料、包装、润滑油、涂料及化肥领域的中国制造企业'),
           ('Financiers for downstream industrial projects','下游工业项目的融资方'),
           ('Free-zone operators and industrial-park developers','自由区运营商及产业园开发商'),
           ('Equipment suppliers for compounding and blending plants','改性造粒及调和工厂的设备供应商')],
  docs=[('Partner brief','合作伙伴简介')],
  sources=[]),

 dict(slug='hilltop-global', name="Hilltop Global Oil and Gas Solutions Int'l Ltd", zh='希尔托普环球油气解决方案国际有限公司',
  kicker=('Upstream · Marginal field', '上游 · 边际油田'),
  lede=('A Benin City-based oil company holding the Alaoma marginal field in the onshore Niger Delta, and seeking investment to bring its heavy crude into production.',
        '一家总部位于贝宁城的石油公司，持有尼日尔三角洲陆上的Alaoma边际油田，正在寻求投资以推动其重质原油投产。'),
  facts=[('Asset','资产','Alaoma field, onshore Niger Delta','Alaoma油田，尼日尔三角洲陆上'),
         ('Licence','许可证','Petroleum Prospecting Licence (PPL) 224, 100% held','石油勘探许可证（PPL）224，100%持有'),
         ('Area','面积','34.06 km², carved out of OML 53','34.06平方公里，由OML 53划出'),
         ('Licence granted','授予日期','28 June 2022','2022年6月28日'),
         ('Product','产品','Heavy crude','重质原油'),
         ('Managing director','董事总经理','Umweni Osarodion Johnbull','Umweni Osarodion Johnbull'),
         ('Head office','总部','45 Old Etete Road, GRA, Benin City, Edo State','埃多州贝宁城GRA区Old Etete路45号')],
  about=[('Hilltop holds PPL 224 over the Alaoma field, awarded under Nigeria\'s marginal field programme. The licence covers 34 km² carved out of OML 53 in the onshore Niger Delta and is registered with the Nigerian Upstream Petroleum Regulatory Commission (NUPRC) as 100% held by Hilltop.',
          'Hilltop持有Alaoma油田的PPL 224许可证，该油田依据尼日利亚边际油田计划授予。许可区面积34平方公里，由尼日尔三角洲陆上的OML 53划出，在尼日利亚上游石油监管委员会（NUPRC）登记为Hilltop 100%持有。'),
         ('The company is seeking an investor to fund the development of the field and the production of its heavy crude.',
          '公司正在寻求投资者，为油田开发及重质原油生产提供资金。')],
  seeking=[('Equity or development finance for the Alaoma field','Alaoma油田的股权投资或开发融资'),
           ('Technical partners with heavy-oil production experience','具有重油开采经验的技术合作伙伴'),
           ('Drilling, well-services and early-production-facility contractors','钻井、井下作业及早期生产设施承包商'),
           ('Crude offtakers','原油承购方')],
  docs=[('Company profile','公司简介')],
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
  kicker=('Gas · Floating LNG and power', '天然气 · 浮式液化天然气与发电'),
  lede=('Developer of the 3 MTPA Ace FLNG and 235 MW power barge offshore Escravos, a US$5.5 billion integrated project to commercialise more than 7 Tcf of Nigerian gas, and of flare-gas projects with NNPC.',
        '埃斯克拉沃斯近海300万吨/年Ace浮式液化天然气（FLNG）及235兆瓦发电驳船的开发商。该综合项目投资55亿美元，旨在开发尼日利亚逾7万亿立方英尺天然气资源；公司还与尼日利亚国家石油公司（NNPC）合作开发燃除气项目。'),
  facts=[('Flagship project','旗舰项目','3 MTPA Ace FLNG and 235 MW power barge','300万吨/年Ace FLNG及235兆瓦发电驳船'),
         ('Location','位置','About 10 km offshore Escravos, Niger Delta','尼日尔三角洲埃斯克拉沃斯近海约10公里'),
         ('Gas resource','天然气资源','Over 7 Tcf of non-associated and associated gas, four concessions within 100 km','逾7万亿立方英尺非伴生气及伴生气，100公里范围内四个区块'),
         ('Gas processed','处理气量','550 MMSCFD wet gas','5.5亿立方英尺/日湿气'),
         ('Output','产出','3 MTPA LNG · 25,000 bopd condensate · 700 t/day LPG · 300 t/day propane','液化天然气300万吨/年 · 凝析油2.5万桶/日 · 液化石油气700吨/日 · 丙烷300吨/日'),
         ('Investment','投资额','About US$5.5 billion, integrated upstream and midstream','约55亿美元，上中游一体化'),
         ('Stage','阶段','FEED; first gas targeted Q2 2030','前端工程设计（FEED）；目标2030年第二季度首气'),
         ('Contact','联系人','Christopher Nwokolo','Christopher Nwokolo')],
  about=[('The Ace FLNG and power barge are collocated to process wet gas from several sources around the Escravos and Forcados hub. The barge supplies power to Ace\'s gas assets and nearby processing facilities; the FLNG delivers LNG for export together with condensate, LPG and propane. At peak the company expects revenue of more than US$2.5 billion a year.',
          'Ace FLNG与发电驳船同址布置，处理埃斯克拉沃斯和福卡多斯枢纽周边多个来源的湿气。发电驳船为Ace的天然气资产及附近处理设施供电；FLNG生产出口液化天然气，同时产出凝析油、液化石油气和丙烷。公司预计高峰期年收入超过25亿美元。'),
         ('Chinese contractor Wison New Energies completed pre-FEED in early 2024 and signed the FEED contract for the FLNG and power barge in December 2024. Liquefaction uses Chart Industries\' IPSMR technology, and Siemens Energy is lined up for power and compression. According to the company, NNPC has committed feedstock gas.',
          '中国承包商惠生新能源（Wison New Energies）于2024年初完成预可研设计（pre-FEED），并于2024年12月签署FLNG及发电驳船的FEED合同。液化工艺采用Chart公司的IPSMR技术，西门子能源负责发电和压缩系统。据公司介绍，NNPC已承诺提供原料气。'),
         ('Ace has also partnered with NNPC on several flare-to-value projects: barge-mounted and land-based flare-to-LNG, and flare gas to low-carbon aviation fuel.',
          'Ace还与NNPC合作开发多个燃除气增值项目：驳船式及陆上燃除气制液化天然气，以及燃除气制低碳航空燃料。')],
  seeking=[('Equity and project finance (over US$1 billion)','股权投资与项目融资（逾10亿美元）'),
           ('LNG offtakers and buyers in China','中国的液化天然气承购方和买家'),
           ('Fabrication, marine and equipment partners for EPC','EPC所需的制造、海工及设备合作伙伴'),
           ('Investors for flare-gas-to-LNG and aviation-fuel projects','燃除气制液化天然气及航空燃料项目的投资者')],
  docs=[('NNPC–Ace FLNG terms of reference','NNPC–Ace FLNG项目任务书'),('Ace Global Refining company profile','Ace Global Refining公司简介'),('Ace upstream portfolio','Ace上游资产组合')],
  sources=[('Gas Processing & LNG: Wison New Energies and Ace Gas & FLNG sign FEED contract','https://www.gasprocessingnews.com/news/2024/12/wison-new-energies-ace-gas-flng-sign-feed-contract-for-nigeria-flng-project/'),
           ('Global Energy Monitor: Ace Gas Nigeria FLNG Terminal','https://gem.wiki/Ace_Gas_Nigeria_FLNG_Terminal')]),
]

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
    out = (TPL.replace('{{NAME}}', E(c['name'])).replace('{{NAME_ZH}}', E(c['zh'])).replace('{{URL}}', url)
           .replace('{{DESC}}', E(desc)).replace('{{KICKER}}', E(c['kicker'][0])).replace('{{KICKER_ZH}}', E(c['kicker'][1]))
           .replace('{{LEDE}}', E(c['lede'][0])).replace('{{LEDE_ZH}}', E(c['lede'][1]))
           .replace('{{FACTS}}', facts).replace('{{ABOUT}}', about).replace('{{SEEKING}}', li(c['seeking']))
           .replace('{{DOCS}}', docs).replace('{{SOURCES}}', src)
           .replace('{{MAILTO}}', f'mailto:{MAIL}?subject={subj}&amp;body={body}')
           .replace('{{SLUG}}', c['slug']).replace('{{JSONLD}}', json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": c['name'], "description": desc, "url": url}, ensure_ascii=False)))
    open(os.path.join(OUT, c['slug'] + '.html'), 'w').write(out)
    print(c['slug'], len(out))
