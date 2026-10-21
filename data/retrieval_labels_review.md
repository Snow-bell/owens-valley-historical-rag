# Retrieval test set: review

For each query, tick the documents a good retrieval should return: ones that substantially answer the question, not ones that merely mention a term. Untick wrong proposals, tick missing ones, or add a line `- [x] <path>` for a document not listed (paths are relative to `data/corpus/`). Tick `none` if no document in the corpus answers the query.

Proposed ticks: found by both the current index and the full-text keyword search; or reranker score ≥ 0.95 in the top 3; or a clear keyword winner. `IX #3 0.99` = rank and reranker score in today's index. `KW #1 p119` = keyword rank and best page. Today's index holds only the first 15k characters of each document, so long books (Story of Inyo, the Steward ethnography, the USGS report) mostly show up only under KW.

Notes after a query (`> note: ...`) are kept.

## 1. What did the Owens Valley Paiute families diet consist of during the winter months?

- [x] ethnography-of-owens-valley-paiute.pdf — IX #1 0.3548 · KW #2 p69 · T1 academic/mild
  - “Steward: Ethnography of Owens Valley Paiute tion.'26 It entailed close friendship, mutual regard, aid, and gifts of food and other things. Parents selected children's spo…”
- [x] owensvalleyhistory/stories__northern paiutes of california and nevada.pdf.pdf — IX #2 0.3306 · KW #7 p40 · T2 none/none
  - “THE NORTHERN PAIUTE INDIANS LIFE IN THE BAND DID THEY HAVE ANY GOVERNMENT? There was no Paiute nation . Paiute is a chance name given by the Whites to a number of Indians…”
- [ ] owensvalleyhistory/stories__armstrong_why_owens_lake_is_red_1981.pdf.pdf — KW #3 p1 · T2 none/none
  - “ts of saline ponds and lakes, were an important food in the diet of local Paiute Indians. The pupae, which look like grains of rice, occur in enormous numbers and can sti…”
- [ ] water-land-history-oviwc.pdf — IX #6 0.0469 · T1 primary_indigenous/none
  - “ the Big Pine Paiute Tribe of the Owens Valley, Bishop Paiute Tribe, Lone Pine Paiute-Shoshone Reservation, and Utu Utu Gwaitu Paiute Tribe established the Owens WATER & …”
- [ ] owensvalleyhistory/stories__where_have_ranches_gone.pdf.pdf — IX #7 0.0354 · T2 none/none
  - “Page 1 of 3 Where Have All The Ranches GoneÉ By Frank Madina Native American pioneer from Independence, CA This is what the city of Los Angeles Water and Power did to Owe…”
- [ ] payahuunadu-oviwc.pdf — IX #8 0.035 · T1 primary_indigenous/none
  - “ Angeles’ interest in the land exchange of 1937, but one of the primary factors was the City’s observation that all water expended upon agriculture limited water availabl…”
- [ ] none

## 2. Describe the landscape of the Owens Valley floor in early spring before the aqueduct was built and the land dried up.

- [x] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — IX #2 0.8326 · KW #3 p6 · T2 none/none
  - “1 POINTS OF INTEREST IN THE OWENS RIVER VALLEY A visit to Californiaʼs Owens River Valley serves as a case study for understanding the reach of the city and the reshaping…”
- [x] owensvalleyhistory/stories__chronological_history_ov.pdf.pdf — IX #3 0.8284 · KW #4 p5 · T2 none/none
  - “Chronological History of Owens Valley Page 5 of 6 1908 The Nevada and California Railroad (now Southern Pacific) extended the Owenyo line north from Mojave into the Owens…”
- [x] owensvalleyhistory/ov_aqueduct__page19.html.txt — IX #9 0.4618 · KW #6 · T2 none/none
  - “to Mojave. He reports over 500,000 acres of good Government land between Keeler and Mojave, all of which will produce anything that can be grown in Los Angeles county, in…”
- [ ] owensvalleyhistory/stories__a_lake_no_more.pdf.pdf — IX #1 0.9041 · T2 none/none
  - “1 A Lake No More Before diversions began, Owens Lake covered over 100 square miles of the Owens Valley floor. Steamships had once plied its water carrying silver bullion …”
- [ ] owensvalleyhistory/stories__An Irishmans Diary about Fr John Crowley.pdf.pdf — KW #1 p2 · T2 none/none
  - “2 It also included the Owens Valley, then still a relatively verdant spread of farmland watered by the Owens River which flowed down from the snow-capped High Sierras. Pa…”
- [ ] owensvalleyhistory/stories__An%20Irishmans%20Diary%20about%20Fr%20John%20Crowley.pdf.pdf — KW #2 p2 · T2 none/none
  - “2 It also included the Owens Valley, then still a relatively verdant spread of farmland watered by the Owens River which flowed down from the snow-capped High Sierras. Pa…”
- [ ] owensvalleyhistory/owens_valley_owens_lake__page99.html.txt — IX #4 0.8269 · T2 none/none
  - “Owens Valley, Owens Lake,Owens River, Bartlett Owens Valley, Owens Lake & Bartlett, CA See on Home Page. Fotocards courtesy of the Rich McCutchan Archives unless otherwis…”
- [ ] owensvalleyhistory/stories__saline_valley_salt_works.pdf.pdf — KW #5 p2 · T2 none/none
  - “Saline Valley Salt Works Page 2 filling 56 gondolas per hour, or 20-24 tons per hour. As many as 40 - 60 men were employed at the salt tram, enduring summer temperatur…”
- [ ] owensvalleyhistory/ov_aqueduct__page18.html.txt — IX #5 0.7507 · T2 none/none
  - “(L-R) John R. Freeman, Joseph D. Schuyler, J.B. Lippincott, Fred P. Stearns, William Mulholland The fruit of all their labor - Owens Valley water pouring down "The Cascad…”
- [ ] owensvalleyhistory/ghosts_of_past2__page9.html.txt — IX #6 0.5535 · T2 none/none
  - “ to fishing because of severe poaching, and giardia was introduced to the streams of the area. What a terrible price to pay for a road to nowhere. Sherman Stevens Sawmill…”
- [ ] geology-and-water-resources-ov-report.pdf — IX #7 0.497 · T3 institutional_bias/mild
  - “-water diversions to the river-aqueduct system. Pumpage from wells needed to supplement water export has increased since 1970, when a second aqueduct was put into service…”
- [ ] none

## 3. Describe where Owens Valley Paiute families lived after they returned from their forced relocation to Fort Tejon.

- [x] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #1 0.9969 · KW #3 p2 · T2 none/none
  - “Allen Matlick History Page 2 There were Paiute Indians living along the Owens River and Bishop Creek. They were a friendly people and few incidents of friction occurred b…”
- [x] payahuunadu-oviwc.pdf — IX #2 0.9848 · KW #2 p4 · T1 primary_indigenous/none
  - “mping. Next, they turned to the lands held in trust for the Paiute by the federal government. Between 1920 and 1930, as agricultural activities decreased due to land sale…”
- [x] ov-native-water-story.pdf — IX #3 0.9681 · KW #9 p1 · T1 primary_indigenous/none
  - “ly forcibly marched by the United States cavalry out of our valley to Fort Tejon, in present-day Tejon Pass, which is north of Los Angeles and south of Bakersfield, Calif…”
- [x] owensvalleyhistory/stories__some early history of owens river valley.pdf.pdf — IX #10 0.5975 · KW #5 p3 · T2 none/none
  - “ng the discoveries made, says : "To one of the lakes I gave Owens* name." He gave the names of several of his band to rivers, creeks and lakes that the expedition discove…”
- [ ] owens-valley-paiute-autobiographies.pdf — KW #1 p13 · T1 academic/mild
  - “steward] AN OWENS VALLEY PAIUTE 195 proposed peace and arranged a big feast at Fort Independence for all the Indians in the region. The Indians arrived, Panatiibiji' amon…”
- [ ] owensvalleyhistory/stories__northern paiutes of california and nevada.pdf.pdf — IX #4 0.9332 · T2 none/none
  - “ is lost in the past , like the movements of so many Indian peoples . Students have divided the Ameri can Indians into various groups, according to language, and when the…”
- [ ] water-land-history-oviwc.pdf — IX #5 0.9311 · T1 primary_indigenous/none
  - “WATER & LAND HISTORY — Owens Valley Indian Water Commission A HISTORY OF WATER RIGHTS & LAND STRUGGLES Time Immemorial The Nüümü have lived in Payahuunadü “Land of the Fl…”
- [ ] story-of-inyo.pdf — KW #4 p180 · T3 settler_bias/moderate
  - “t to hit. Still Whitson refused to escape, and was taken to Fort Tejon, where he was kept for a few months and finally released. With such happenings as this and the Kern…”
- [ ] ethnography-of-owens-valley-paiute.pdf — IX #8 0.8629 · KW #10 p11 · T1 academic/mild
  - “Steward: Ethnography of Owens Valley Paiute Sierra to a line running out into Owens valley from waucodayavi, the largest peak south of Rawson creek; iitii'iitii witu (als…”
- [ ] owensvalleyhistory/bishop_residents2__page48cc.html.txt — IX #6 0.9268 · T2 none/none
  - “Owens Valley Shoshone - Paiutes Owens Valley Paiute - Bishop, CA Owens Valley Shoshone - Paiutes Bishop - 5 Joe Bowers - Owens Valley Paiute (Courtesy J.D. Black Collecti…”
- [ ] owensvalleyhistory/stories__plea_for_help.pdf.pdf — KW #6 · T2 none/none
  - “on Bishop, his wife, and several hired hands arrived in the Owens Valley on August 22, 1861 from Fort Tejon in the Tehachapi Mountains. Bishop and his wife were some of t…”
- [ ] owensvalleyhistory/independence__page69.html.txt — IX #7 0.9182 · T2 none/none
  - “Pack Train heading up Kearsarge Pass Pack Train heading up Kearsarge Pass Snow covered Onion Valley Road Owens Valley - 1931 Snow covered Onion Valley Road Owens Valley -…”
- [ ] none

## 4. How did the LA aqueduct project affect water access for Owens Valley residents?

- [x] owensvalleyhistory/ov_aqueduct__page20c.html.txt — IX #2 0.9935 · KW #4 · T2 none/none
  - “ch a situation lies in joining with Los Angeles in bringing water from the Colorado river, and by so doing water now in use for irrigation of farming and orchard lands ca…”
- [x] owensvalleyhistory/ov_aqueduct__page19.html.txt — IX #9 0.9802 · KW #2 · T2 none/none
  - “- 1929 Owens River winding its way through Owens Valley Regulating gates on main canal in Owens Valley - 1912 Transformer float for Dredge No. 4l in Owens Valley - 190…”
- [x] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #7 0.9898 · KW #5 p3 · T2 none/none
  - “Valley of Broken Hearts – Part 2 3 SETTLERS INDIGNANT The first indignation, naturally, was over the losing of the government reclamation project. This project…”
- [x] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — IX #13 0.9654 · KW #1 p7 · T2 none/none
  - “was sharply reduced. Increasing demand by the city for more water prompted the DWP to construct a second aqueduct during the 1960s. Without the publicity and fanfare that…”
- [ ] owensvalleyhistory/stories__aqueduct_history.pdf.pdf — IX #4 0.9913 · KW #9 p2 · T2 none/none
  - “L. A. Aqueduct History Told 2 This reservoir is the only storage provided by the Mulholland project within Owens Valley. Haiwee serves the double purpose of providing…”
- [ ] ov-native-water-story.pdf — IX #1 0.9942 · T1 primary_indigenous/none
  - “. Because they had stolen the rich soils of our homeland, we moved to the sites, we began to make homes in the areas we once lived on and became day laborers for the whit…”
- [ ] owensvalleyhistory/stories__never_the_same.pdf.pdf — IX #3 0.9935 · T2 none/none
  - “Things Will Never Quite be the Same The City of Los Angeles quickly and quietly began the process of acquiring water rights through permits, condemnations and outright la…”
- [ ] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — KW #3 p7 · T2 none/none
  - “n preliminary anyway, withdrew its plans for a contemplated Owens Valley reclamation project. Angry Owens Valley residents branded Lippincott as "Judas B. Lippincott." Li…”
- [ ] owensvalleyhistory/jd_black_collection__page20e.html.txt — IX #5 0.991 · T2 none/none
  - “J.D. Black Scrapbook Owens Valley's - Los Angeles Aqueduct All photographs on this pags are from the J. D. Black Collection digital archives located in the unless otherwi…”
- [ ] owensvalleyhistory/ov_aqueduct__page18.html.txt — IX #8 0.9867 · T2 none/none
  - “Los Angeles Aqueduct - The Grand Plan Owens Valley's - Los Angeles Aqueduct See on Home Page. Unless otherwise note, All L.A. aqueduct photographs on these pages are from…”
- [ ] california-geography-ch5-water.pdf — KW #6 p14 · T3 academic/none
  - “the Inyo County bank collapsed, which massively undermined valley resistance. An audit revealed that there were shortages in both cash in the vault and amounts shown on t…”
- [ ] none

## 5. What role did women's clubs play in California civic life in the early 1900s?

- [x] womens-club-biographies/Clara-Burdette.pdf — IX #2 0.9807 · KW #2 · T2 none/none
  - “n clubwoman and philanthropist, and a resident of Pasadena, California. Clara Burdette was the first president of the California Federation of Women's Clubs when it was f…”
- [x] womens-club-biographies/Laura-White.pdf — IX #1 0.9942 · KW #4 · T2 none/none
  - “White was an American activist, best known for founding the California Club, working to preserve groves of redwoods in California, and promoting the City Beautiful moveme…”
- [x] womens-club-biographies/Adella-Schloss.pdf — IX #4 0.9154 · KW #3 · T2 none/none
  - “9, Adella Tuttle married Aaron Schloss, 23, in Watsonville, California; the Schlosses would spend the rest of their lives living first in San Francisco and later in Berke…”
- [x] womens-club-biographies/Ione-Cowles.pdf — IX #7 0.567 · KW #5 · T2 none/none
  - “eighth international president of the General Federation of Women's Clubs. She served for two administrations: 1916-1918 and 1918-1920. Cowles was born on March 13, 1858 …”
- [ ] womens-club-biographies/Lotta-Hetler-James.pdf — IX #9 0.2404 · KW #1 · T2 none/none
  - “ta Hetler James (1876-1945) was a public speaker; active in civic, church and community projects; and a candidate for Governor of California. Lotta Hetler was born in Chi…”
- [ ] womens-club-biographies/Orr-Kimberly-Shirk.pdf — IX #3 0.9532 · T2 none/none
  - “Eliza A. Orr served as President of the California Federation of Women’s Clubs from 1912 to 1914. During her administration, Political Science, Peace, Literature and Coun…”
- [ ] womens-club-biographies/Caroline-Severance.pdf — IX #5 0.8595 · KW #10 · T2 none/none
  - “s Public Library. In 1878 she founded the first Los Angeles Women's Club. Her interests were far ranging, from woman suffrage to historic preservation [working with Charl…”
- [ ] womens-club-biographies/Mariana-Bertola.pdf — IX #8 0.3953 · KW #6 · T2 none/none
  - “Dr. Mariana Bertola was born in Pacheco, California, the daughter of Italian immigrant parents. Mariana attended San Jose State Normal School and, later, Cooper Medical C…”
- [ ] womens-club-biographies/MaryBarnum-Ellen-Sargent.pdf — IX #6 0.8078 · T2 none/none
  - “Mary Gilmore Barnum (1869- ) Mary Gilmore Barnum was born in Grinnell, Iowa in 1869. Mary graduated from Los Angeles High School and the University of California, Los Ang…”
- [ ] none

## 6. Describe the general geology of Owens Valley.

- [x] geology-and-water-resources-ov-report.pdf — IX #1 0.9981 · KW #2 p115 · T3 institutional_bias/mild
  - “p. Bateman, P.C., Erickson, M.P., and Proctor, P.D., 1950, Geology and tungsten deposits of the Tungsten Hills, Inyo County, California: Journal of Mines and Geology, Cal…”
- [x] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — IX #11 0.5034 · KW #4 p24 · T2 none/none
  - “19 POINTS OF INTEREST IN THE OWENS RIVER VALLEY EASTERN SIERRA INTERAGENCY INFORMATION CENTER The Eastern Sierra Interagency Information Center provides information on th…”
- [x] owensvalleyhistory/owens_valley_owens_lake__page99.html.txt — IX #9 0.6125 · KW #9 · T2 none/none
  - “Owens Lake, viewed from the road Irrigation Map of Owens Valley - 1922 (Map courtesy of ) by John R. Dyni and Richard W. Jones Bartlett (Photo courtesy of Larry…”
- [ ] owensvalleyhistory/stories__Inyo County by Sunset Magazine_june 1912.pdf.pdf — IX #5 0.9384 · T2 none/none
  - “ of over ten thousand to twelve thousand feet . Through the center of the county , from north to south on a parallel with the Sierra Nevadas and divided from them by Owen…”
- [ ] owensvalleyhistory/stories__Marius Campbell 1902 geological report.pdf.pdf — KW #1 p24 · T2 none/none
  - “INDEX. Page. Arnargosa Valley, geology near............ 14-16 Ash Meadows, geology near................ 16 Borate, geology near ....................... 12-13 Borax indust…”
- [ ] owensvalleyhistory/stories__Life in Southern California_The Gentleman's Magazine_january to june 1894.pdf.pdf — IX #6 0.8911 · T2 none/none
  - “ chains from the Sierras to the Rockies. This is the home of the Puite and the Shoshonee, of the “ side-winder ” rattlesnake, and of the horned toad. The hills are rich i…”
- [ ] owensvalleyhistory/stories__backroad tours in inyo county.pdf.pdf — KW #3 p49 · T2 none/none
  - “ineages, contemporary weavers, and basket collectors of the Owens Valley. General Guides California’s Eastern Sierra: A Visitor’s Guide Sue Irwin Cachuma Press, 1991 Feat…”
- [ ] owensvalleyhistory/ov_aqueduct__page20a.html.txt — KW #5 · T2 none/none
  - “ready to conneot it up with the Southern Pacific at Mojave. General Manager Bancroft and General Superintendent Buckingham of the Oregon Short Line, and General Superinte…”
- [ ] owensvalleyhistory/stories__some early history of owens river valley.pdf.pdf — IX #7 0.6545 · T2 none/none
  - “ 1854 at $600,000. Owens River Valley was supposed to be one of the retreats of the Horse Thief Indians, the name by which these mountain and desert Indians were generall…”
- [ ] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — KW #6 p8 · T2 none/none
  - “case. In the long run, if one looks for winners and losers, Owens Valley may have come out slightly ahead. Visitors to the Owens Valley tourist information centers find d…”
- [ ] owensvalleyhistory/stories__riverside_daily_press.pdf.pdf — IX #8 0.6317 · T2 none/none
  - “1 River#ide Daily Pre## THURSDAY, JULY 7, 1892 The Owens River Valley. (by Fred Eaton) (Article courtesy of Hal Eaton) Fred Eaton of Los Angeles has just returned from an…”
- [ ] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #10 0.6036 · T2 none/none
  - “1 STRUGGLE FOR WATER IN OWENS VALLEY IS TOLD BY CALL STAFF WRITER Here is the second of a series of dramatic fact stories of the tragedy that has overtaken the Owens Rive…”
- [ ] none

## 7. Describe the eastern Sierra Nevada mountain passes and terrain.

- [x] owensvalleyhistory/stories__backroad tours in inyo county.pdf.pdf — IX #1 0.9512 · KW #2 p3 · T2 none/none
  - “3 WELCOME TO THE HIGH PASSES, BACK REACHES, SIDE ROADS AND HIDDEN CORNERS OF THE EASTERN SIERRA AND DEATH VALLEY! SPECTACULARLY SCENIC INYO COUNTY, CALIFORNIA HAS SOME OF…”
- [x] owensvalleyhistory/stories__the_passes.pdf.pdf — IX #3 0.7544 · KW #3 p1 · T2 none/none
  - “Page 1 of 8 T The Passes By John Muir he sustained grandeur of the High Sierra is strikingly illustrated by the great height of the passes. Between latitude 36° 20' and 3…”
- [x] fauna-flora-ov.pdf — IX #7 0.6306 · KW #1 p5 · T2 none/none
  - “ength and beauty.” –John Muir In 1995 the population of the Sierra Nevada Bighorn Sheep hit an all time low of 100 individuals despite efforts by the California Departmen…”
- [ ] owensvalleyhistory/sierra_names3__page66a.html.txt — IX #2 0.7788 · T2 none/none
  - “Spanish and Indian Place Names of the Sierra Nevada Spanish and Indian Place Names of the Sierra Nevada Sequoia National Forest & Sierra National Forest maps courtesy of …”
- [ ] owensvalleyhistory/stories__Horse Meadows and Bohler Canyon Arborglyphs.pdf.pdf — KW #4 p2 · T2 none/none
  - “r lamb, mutton and wool. Fred Fulstone, member of a pioneer Nevada ranching family, is convinced that the early miners could not have endured the harsh working conditions…”
- [ ] owensvalleyhistory/sierra_names1__page66.html.txt — IX #4 0.7226 · T2 none/none
  - “a] Sierra Nevada crest from just east of Lone Pine, CA [Photo courtesy of Ray DeLea] is Spanish for "snowy mountain range." Sierra is the word for "saw," and when used in…”
- [ ] owensvalleyhistory/stories__owens_valley_rock_art.pdf.pdf — KW #5 p124 · T2 none/none
  - “states that no specimens of deer are now found in the White Mountain area of southern Esmeralda County, Nevada. Yet at site Es-l, between the Old Davis Ranch and Trail Ca…”
- [ ] california-geography-ch12-great-basin.pdf — KW #6 p13 · T3 academic/none
  - “ed by a combination of faulting and erosion. Initially, the Sierra Nevada mountains were formed by the subduction of the Pacific Plate beneath the North American Plate. T…”
- [ ] owensvalleyhistory/stories__tails_of_the_trails.pdf.pdf — IX #9 0.3975 · T2 none/none
  - “Across the Range of Light One of the great adventures in the High Sierra is to cross the Sierra Nevada range on horseback. Red's Mea­dow Pack Station provides the opportu…”
- [ ] owensvalleyhistory/stories__samuel%20d%20woods_summer%20jaunt%20in%20the%20high%20sierras.pdf.pdf — IX #12 0.3088 · T2 none/none
  - “ , A WHITE MAN AND A NEGRO 404 XXIII . INCIDENTS OF FRONTIER LIFE 420 XXIV. Two GREAT SAERIFFS 435 XXV. A TRANSPLANTED RAILROAD AND THE MAN WHO TRANSPLANTED IT 455 . Chap…”
- [ ] owensvalleyhistory/stories__streets_of_the_mountains.pdf.pdf — IX #13 0.2809 · T2 none/none
  - “Page 1 of 4 A The Streets of the Mountains By Mary Austin LL STREETS of the mountains lead to the citadel; steep or slow they go up to the core of the hills. Any trail th…”
- [ ] none

## 8. How did Los Angeles justify the acquisition of Owens Valley water rights?

- [x] ov-native-water-story.pdf — IX #3 0.9947 · KW #1 p2 · T1 primary_indigenous/none
  - “hop, Big Pine and Lone Pine Tribes had a valid claim to the water rights associated with the 1937 Land Exchange. We were not receiving all the water we were entitled to o…”
- [x] owensvalleyhistory/ov_aqueduct__page20c.html.txt — IX #1 0.9965 · KW #4 · T2 none/none
  - “seeking to justify their course that liberal prices have been paid for Owens Valley property. Considering land and buildings only, and with some exceptions, that is true.…”
- [x] water-land-history-oviwc.pdf — IX #4 0.9936 · KW #2 p3 · T1 primary_indigenous/none
  - “Valley Indian Water Commission (“Commission”) in 1991. The Fort Independence Reservation joined membership in the Commission in 1992. Since its inception, the C…”
- [x] owensvalleyhistory/ov_aqueduct__page19.html.txt — IX #7 0.9872 · KW #7 · T2 none/none
  - “the present water suit against the city. With such a small proportion of lands left unpurchased in both counties, it seems strange that the City does not execute its purc…”
- [ ] owensvalleyhistory/stories__never_the_same.pdf.pdf — IX #2 0.9952 · T2 none/none
  - “Things Will Never Quite be the Same The City of Los Angeles quickly and quietly began the process of acquiring water rights through permits, condemnations and outright la…”
- [ ] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — KW #3 p6 · T2 none/none
  - “side information to buy up 16,000 acres of the San Fernando Valley that would be irrigated with Owens River water. In 1905 the San Fernando Valley was a sparsely settled,…”
- [ ] payahuunadu-oviwc.pdf — IX #8 0.9869 · T1 primary_indigenous/none
  - “’s resources and carefully harvested its seed concentrations in order to sustain the land while living upon it. This was a longstanding, ecologically sustainable means of…”
- [ ] california-geography-ch5-water.pdf — KW #5 p12 · T3 academic/none
  - “Obtaining Water Rights - 1902–1907 At the start of the 20th century, the United States Bureau of Reclamation, at the time known as the United States Reclamation Service,…”
- [ ] owensvalleyhistory/stories__police_ready.pdf.pdf — IX #13 0.9769 · T2 none/none
  - “ Valley. Its tax bill for the present year amounted to $144,000 or 43 percent of the total county taxes. Ever since the Aqueduct was placed in operation, the city of Los …”
- [ ] chronicling-america/stealing-owens-river-supply-july-30-1905.pdf — KW #6 · T2 institutional_bias/severe
  - “ers at work consider- ingithe proposition of conserving the water,', but through the efforts of En- gineer J. B. Llpplncott this Idea was given.up land' the land turned o…”
- [ ] owensvalleyhistory/ghosts_of_past2__page9.html.txt — IX #15 0.9767 · T2 none/none
  - “wrote: "Los Angeles gets its water by reason of one of the costliest, crookedest, most unscrupulous deals ever perpetrated, plus one of the greatest pieces of engineering…”
- [ ] none

## 9. What flora and fauna were native to the Owens Valley region?

- [x] fauna-flora-ov.pdf — IX #1 0.9991 · KW #1 p2 · T2 none/none
  - “the export of water from the valley by the city of Los Angeles. The loss of water and recession of the vast underground aquifer below this region (which is a story for an…”
- [x] owensvalleyhistory/stories__backroad tours in inyo county.pdf.pdf — IX #9 0.3183 · KW #2 p47 · T2 none/none
  - “inued on page 48 Natural History Geology Underfoot in Death Valley and Owens Valley Robert P. Sharp and Allen F. Glazner Mountain Press, 1997 This is a must-have for anyo…”
- [ ] payahuunadu-oviwc.pdf — KW #3 p3 · T1 primary_indigenous/none
  - “Our Ecology Prior to Western Contact The Nüümü (Owens Valley Paiute) are a people born of water. Our oral histories, passed down from generation to generation, tell of th…”
- [ ] california-geography-ch12-great-basin.pdf — KW #4 p21 · T3 academic/none
  - “Flora & Fauna The flora of the Mojave Desert consists of various endemic plant species, notably the Joshua Tree, which is a notable endemic and indicator specie…”
- [ ] ethnography-of-owens-valley-paiute.pdf — IX #6 0.6182 · T1 academic/mild
  - “ performances . . . . . . . . . . . . . . . . 313 Other curing . . . . . . . . . 316 Medicinal plants . . . . . . . . . . . . . . . . . . . 317 Jimsonweed.. . ...........…”
- [ ] owensvalleyhistory/stories__death valley men_COMPRESSED.pdf.pdf — KW #5 p6 · T2 none/none
  - “138 DEATH VALLEY MEN an give 'em to you right on the sidewalk in front a your bank!' «An he says, ·wait a minute!' An we talked some more an he finally give me some more…”
- [ ] story-of-inyo.pdf — KW #6 p380 · T3 settler_bias/moderate
  - “Geological Survey, re- marks that the Piute name for Death Valley is **Tomesha," meaning ''ground afire." Those Piutes have sometimes graphic descriptive powers. Fog is o…”
- [ ] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — IX #14 0.1023 · KW #8 p31 · T2 none/none
  - “POINTS OF INTEREST IN THE OWENS RIVER VALLEY 26 Built in 1917, the Mt. Whitney Fish Hatchery is the earliest and the grandest of the hatcheries in the valley. Game fish s…”
- [ ] owensvalleyhistory/stories__where_have_ranches_gone.pdf.pdf — IX #7 0.3845 · T2 none/none
  - “Page 1 of 3 Where Have All The Ranches GoneÉ By Frank Madina Native American pioneer from Independence, CA This is what the city of Los Angeles Water and Power did to Owe…”
- [ ] owensvalleyhistory/stories__Life in Southern California_The Gentleman's Magazine_january to june 1894.pdf.pdf — IX #10 0.2792 · T2 none/none
  - “ chains from the Sierras to the Rockies. This is the home of the Puite and the Shoshonee, of the “ side-winder ” rattlesnake, and of the horned toad. The hills are rich i…”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #12 0.2058 · T2 none/none
  - “ordo Freighting company, based in Mojave, California. His travels took him through Bishop in the beautiful Owens Valley. It captivated Al from the moment he first saw it.…”
- [ ] owensvalleyhistory/my_owens_valley__page89.html.txt — IX #13 0.1146 · T2 none/none
  - “My Owens Valley "My Owens Valley" All photos are courtsey of and copyright by Ray DeLea (" ") unless otherwise noted. The following are photographs I have taken in and ar…”
- [ ] none

## 10. How did Paiute communities respond to land dispossession?

- [ ] owensvalleyhistory/stories__northern paiutes of california and nevada.pdf.pdf — IX #8 0.0015 · KW #1 p72 · T2 none/none
  - “s situation . The city proposed to take over all the Indian lands, except Fort Independence, which is still usable and to give the Indians instead , 1470 acres of the ric…”
- [ ] ov-native-water-story.pdf — IX #11 0.0008 · KW #2 p2 · T1 primary_indigenous/none
  - “ng the Fort Independence Reservation and the Utu Utu Gwaitu Paiute Tribe on environmental protection. The Tribes recognize their common goals of healthy communities and e…”
- [ ] geology-and-water-resources-ov-report.pdf — KW #3 p22 · T3 institutional_bias/mild
  - “logical data and ranged from 12 in. in alkaline scrub plant communities to 41 in. in alkaline meadow plant communities (Duell, 1988). Plant studies by Groeneveld and othe…”
- [ ] water-land-history-oviwc.pdf — IX #3 0.0081 · KW #4 p3 · T1 primary_indigenous/none
  - “se it lacked access to “wet” water, infrastructure funding, land acquisition, and the usual benefits found in water settlements. The agreement was essentially a “paper” w…”
- [ ] owensvalleyhistory/coso_hot_springs__page98.html.txt — KW #5 · T2 none/none
  - “t only attracted visitors from nearby eastern Sierra Nevada communities, but the rising popularity of auto travel quickly changed everything. People started coming to the…”
- [ ] payahuunadu-oviwc.pdf — IX #1 0.0209 · KW #6 p4 · T1 primary_indigenous/none
  - “ty also began groundwater pumping. Next, they turned to the lands held in trust for the Paiute by the federal government. Between 1920 and 1930, as agricultural activitie…”
- [ ] owensvalleyhistory/stories__The Ever-Changing World of the Paiute.pdf.pdf — IX #9 0.0012 · KW #8 p2 · T2 none/none
  - “homeland in which they dwelt. The tie between the people and the land was of such intimate bonding that it continues to remain a hurtful subject when our people rem…”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #5 0.0028 · T2 none/none
  - “ordo Freighting company, based in Mojave, California. His travels took him through Bishop in the beautiful Owens Valley. It captivated Al from the moment he first saw it.…”
- [ ] owensvalleyhistory/stories__time_changes.pdf.pdf — IX #6 0.0025 · T2 none/none
  - “Times Change for Everyone It's estimated that as many as 2,000 Native Americans called Inyo and the Eastern Sierra home when white European settlers first arrived m the m…”
- [ ] owensvalleyhistory/stories__historic legends_COMPRESSED.pdf.pdf — IX #7 0.0025 · T2 none/none
  - “ured near Bishop where the redmen had a large camp. The retaliation shook up the ranchers to no smal I extent and they called for a summit meeting. Chief George of the Pa…”
- [x] none

## 11. What were the environmental consequences of the aqueduct diversion?

- [x] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — KW #1 p6 · T2 none/none
  - “y residents resorted to violence. Between 1924 and 1927 the aqueduct was dynamited at least a dozen times. Local au­ thorities proved apathetic about tracking down the cu…”
- [ ] owensvalleyhistory/ov_aqueduct__page18.html.txt — IX #5 0.0083 · KW #2 · T2 none/none
  - “rld will never forget." None of us would have to suffer the consequences of such water gluttony if, as Clint Eastwood would say, "Los Angeles would just know its limitati…”
- [ ] geology-and-water-resources-ov-report.pdf — IX #1 0.7246 · T3 institutional_bias/mild
  - “-water diversions to the river-aqueduct system. Pumpage from wells needed to supplement water export has increased since 1970, when a second aqueduct was put into service…”
- [ ] owensvalleyhistory/ov_aqueduct__page19.html.txt — KW #3 · T2 none/none
  - “ft across / 12 ft deep - 1912 Alabama Hills section of the aqueduct. Steam shovel No. 12 Cottonwood conduit showing forms - 1907 Beginning of the Cottonwood conduit showi…”
- [ ] owensvalleyhistory/stories__Los_Angeles_Department_of_Water_and_Power_Operations_in_the_Mono_Basin.pdf.pdf — IX #2 0.073 · KW #5 p7 · T2 none/none
  - “HE LAKE LEVEL. THIS ALTERNATIVE HAS VERY HIGH FINANCIAL AND ENVIRONMENTAL COSTS ASSOCIATED WITH PURCHASING REPLACEMENT WATER AND ENERGY. THE DIRECT COST OF PURCHASING 100…”
- [ ] owensvalleyhistory/stories__monobasinproject.pdf.pdf — KW #4 p2 · T2 none/none
  - “FIG. 1. rvrONO BASIN EXTENSION OF Los ANGELES AQUEDUCT 3°7 Scale In Miles ? Ej 1,2 ·-------- "''\;''''~-~-------_~-._-II /' .""-.- A . .-._......... ",..../.:....--' ."""…”
- [ ] fauna-flora-ov.pdf — KW #6 p7 · T2 none/none
  - “is definitely a survivor. The Fish Slough Area of Critical Environmental Concern (ACEC) is one of the best places to view the pupfish. According to the Bureau of Land Man…”
- [ ] california-geography-ch5-water.pdf — IX #7 0.004 · T3 academic/none
  - “) of land resulting from groundwater extraction. It is a growing problem in the developing world as cities increase in population and water use, without adequate pumping …”
- [ ] owensvalleyhistory/stories__aqueduct_history.pdf.pdf — IX #8 0.0034 · T2 none/none
  - “1 L. A. AQUEDUCT HISTORY IS TOLD Here is the eighth of a series of dramatic fact stories of the tragedy that has overtaken the Owens River Valley in Inyo County, where al…”
- [ ] ov-native-water-story.pdf — IX #9 0.0029 · T1 primary_indigenous/none
  - “. Because they had stolen the rich soils of our homeland, we moved to the sites, we began to make homes in the areas we once lived on and became day laborers for the whit…”
- [ ] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #10 0.0012 · T2 none/none
  - “ miles of desert. To the relinquishment of water for Los Angeles domestic use the people of Owens Valley have long since been reconciled. But to the use of this water for…”
- [ ] owensvalleyhistory/ov_aqueduct__page20c.html.txt — IX #11 0.001 · T2 none/none
  - “ Dynamite Parties "Dynamiters gave the aqueduct little rest during June and July of 1927, six different blasts occurring. The most serious in effects was at a canyon near…”
- [ ] none

## 12. How did Owens Valley Paiute families live after settlers took over Owens Valley?

- [x] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #1 0.9962 · KW #1 p2 · T2 none/none
  - “Allen Matlick History Page 2 There were Paiute Indians living along the Owens River and Bishop Creek. They were a friendly people and few incidents of friction occurred b…”
- [x] payahuunadu-oviwc.pdf — IX #3 0.9701 · KW #3 p4 · T1 primary_indigenous/none
  - “aintained in our use of water and land was interrupted when settlers came into the valley in the 19 th century. Settlers did not recognize the form of agriculture practic…”
- [x] owensvalleyhistory/stories__northern paiutes of california and nevada.pdf.pdf — IX #5 0.8192 · KW #4 p40 · T2 none/none
  - “THE NORTHERN PAIUTE INDIANS LIFE IN THE BAND DID THEY HAVE ANY GOVERNMENT? There was no Paiute nation . Paiute is a chance name given by the Whites to a number of Indians…”
- [x] water-land-history-oviwc.pdf — IX #2 0.9861 · T1 primary_indigenous/none
  - “WATER & LAND HISTORY — Owens Valley Indian Water Commission A HISTORY OF WATER RIGHTS & LAND STRUGGLES Time Immemorial The Nüümü have lived in Payahuunadü “Land of the Fl…”
- [ ] ethnography-of-owens-valley-paiute.pdf — IX #10 0.5074 · KW #2 p69 · T1 academic/mild
  - “Steward: Ethnography of Owens Valley Paiute tion.'26 It entailed close friendship, mutual regard, aid, and gifts of food and other things. Parents selected children's spo…”
- [ ] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #8 0.5624 · KW #9 p3 · T2 none/none
  - “Valley of Broken Hearts – Part 2 3 SETTLERS INDIGNANT The first indignation, naturally, was over the losing of the government reclamation project. This project…”
- [ ] story-of-inyo.pdf — KW #5 p148 · T3 settler_bias/moderate
  - “ground. He had no provisions except what he procured in the valley—a singular condition which he attributed to his having distributed sup- plies to needy settlers—and was…”
- [ ] owensvalleyhistory/stories__chronological_history_ov.pdf.pdf — KW #6 p1 · T2 none/none
  - “Page 1 of 6 Chronological History of Owens Valley Condensed from an excerpt compiled by Al Gagnon 20,000 years ago Before the white man found the Antelope Valley, Fremont…”
- [ ] owensvalleyhistory/independence__page69.html.txt — IX #6 0.6339 · T2 none/none
  - “Pack Train heading up Kearsarge Pass Pack Train heading up Kearsarge Pass Snow covered Onion Valley Road Owens Valley - 1931 Snow covered Onion Valley Road Owens Valley -…”
- [ ] ov-native-water-story.pdf — IX #7 0.5757 · T1 primary_indigenous/none
  - “ M. von Schmidt’s 1855-56 survey of the Owens Valley for the federal government. As part of his report for the state, he created this map which shows the irrigated areas …”
- [ ] owensvalleyhistory/bishop_residents2__page48cc.html.txt — IX #9 0.5383 · T2 none/none
  - “Owens Valley Shoshone - Paiutes Owens Valley Paiute - Bishop, CA Owens Valley Shoshone - Paiutes Bishop - 5 Joe Bowers - Owens Valley Paiute (Courtesy J.D. Black Collecti…”
- [ ] none

## 13. What were some ethical and moral dilemmas created by LA's approach to the aqueduct?

- [ ] owensvalleyhistory/stories__time_changes.pdf.pdf — KW #1 · T2 none/none
  - “lley area of Inyo County. Reservation lands were eventually created for all the tribes in an attempt to give the local Paiute - Shoshone some form of economic stability. …”
- [ ] owensvalleyhistory/stories__greatest_good.pdf.pdf — KW #2 · T2 none/none
  - “Los Angeles were already well aware of possible sources for LA's growing water needs. Fred Eaton was a brilliant young man who became superintendent of the Los Angeles Ci…”
- [ ] owensvalleyhistory/stories__Los_Angeles_Department_of_Water_and_Power_Operations_in_the_Mono_Basin.pdf.pdf — KW #3 p7 · T2 none/none
  - “ATER WOULD BE MORE THAN $9 MILLION ANNUALLY TODAY AND WOULD APPROACH $20 MILLION PER YEAR IN THE FUTURE. THE CALIFORNIA AQUEDUCT MAY NOT BE A RELIABLE SOURCE OF REPLACEME…”
- [ ] ov-native-water-story.pdf — IX #2 0.182 · KW #6 p3 · T1 primary_indigenous/none
  - “Valley Indian Water Commission and some of the artwork was created by the Aqueduct Between Us project. Payahǖǖnadǖ Water Story – Wading Through the Past https://pressbook…”
- [ ] owensvalleyhistory/ov_aqueduct__page20b.html.txt — IX #1 0.6149 · T2 none/none
  - “Los Angeles Aqueduct - Desert and City Owens Valley's - Los Angeles Aqueduct Unless otherwise note, All L.A. aqueduct photographs on these pages are from the unless other…”
- [ ] owensvalleyhistory/stories__samuel woods_three heroes_big pine.pdf.pdf — KW #4 p12 · T2 none/none
  - “out of moral…”
- [ ] owensvalleyhistory/stories__japanese comfort women.pdf.pdf — KW #5 p6 · T2 none/none
  - “behalf of the survivors in order to inform the public, and created Facebook pages. One young man painted a portrait of a comfort woman, showing a single face divided in h…”
- [ ] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — IX #6 0.0415 · KW #8 p5 · T2 none/none
  - “cement of his own fortune. Eaton’s idea was to construct an aqueduct linking the Owens River to Los Angeles. Enter the wild card in the creation of the water controversy:…”
- [ ] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — IX #4 0.0494 · KW #10 p7 · T2 none/none
  - “city for more water prompted the DWP to construct a second aqueduct during the 1960s. Without the publicity and fanfare that accompanied the building of the first aqueduc…”
- [ ] owensvalleyhistory/stories__never_the_same.pdf.pdf — IX #3 0.058 · T2 none/none
  - “Things Will Never Quite be the Same The City of Los Angeles quickly and quietly began the process of acquiring water rights through permits, condemnations and outright la…”
- [ ] owensvalleyhistory/stories__aqueduct_history.pdf.pdf — IX #8 0.0306 · T2 none/none
  - “1 L. A. AQUEDUCT HISTORY IS TOLD Here is the eighth of a series of dramatic fact stories of the tragedy that has overtaken the Owens River Valley in Inyo County, where al…”
- [ ] owensvalleyhistory/ov_aqueduct__page20c.html.txt — IX #9 0.0305 · T2 none/none
  - “ers on one side and the great city of Los Angeles on the Other. It is a drama that has been enacted on a smaller scale many times in California, with water as the cause o…”
- [ ] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #10 0.0258 · T2 none/none
  - “, the metropolis of the valley, began to have dreams of becoming a city of twenty or thirty thousand people. PEOPLE ‘DOUBLE-CROSSED’ This dream received its first jolt wh…”
- [x] none

## 14. Who were some notable families or people in the creation of settler communities in Owens Valley?

- [ ] story-of-inyo.pdf — KW #1 p346 · T3 settler_bias/moderate
  - “ny other advances have come since—further improvements, the creation of first a local telephone system, then its exten- sion through the valley, then connection with the …”
- [ ] owensvalleyhistory/stories__message_from_owens_valley.pdf.pdf — KW #2 p3 · T2 none/none
  - “A Message from Owens Valley 3 Let all isolated communities take warning from the fate of Owens Valley. Le them all join in demanding a broad gauge water program, and in d…”
- [ ] california-geography-ch12-great-basin.pdf — KW #3 p17 · T3 academic/none
  - “abama Hills is Mobius Arch, which is a complete loop. Other notable arches include Lathe Arch, the Eye of Alabama, and Whitney Portal Arch. In addition to their geologica…”
- [ ] owensvalleyhistory/our_world2__page15.html.txt — KW #4 · T2 none/none
  - “ficult task to resettle the West Coast as Japanese American families were faced with racism and discrimination in housing and employment. Many were able only to find dome…”
- [ ] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #9 0.0455 · KW #5 p3 · T2 none/none
  - “Valley of Broken Hearts – Part 2 3 SETTLERS INDIGNANT The first indignation, naturally, was over the losing of the government reclamation project. This project…”
- [ ] ov-native-water-story.pdf — IX #2 0.1988 · KW #8 p1 · T1 primary_indigenous/none
  - “st rate with fine grasses and noted that large areas of the valley were being irrigated. Figure 2: Von Schmidt map. The Owens Valley Indian Water Commission. In 1859 Capt…”
- [ ] owensvalleyhistory/stories__The Ever-Changing World of the Paiute.pdf.pdf — KW #6 p2 · T2 none/none
  - “nging World of the Paiute Joseph Lent1 In the early days of creation the earth was covered with water… This is the beginning of the oldest known origin history which was …”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #11 0.0382 · KW #9 p2 · T2 none/none
  - “k History Page 2 There were Paiute Indians living along the Owens River and Bishop Creek. They were a friendly people and few incidents of friction occurred between them …”
- [ ] owensvalleyhistory/stories__chronological_history_ov.pdf.pdf — IX #1 0.2225 · T2 none/none
  - “Page 1 of 6 Chronological History of Owens Valley Condensed from an excerpt compiled by Al Gagnon 20,000 years ago Before the white man found the Antelope Valley, Fremont…”
- [ ] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — IX #3 0.1882 · T2 none/none
  - “ a roundabout route at best for Eastern Sierra residents. With the beginning of the 20th century, a new opportunity promised to provide a market for Owens Valley products…”
- [ ] owensvalleyhistory/stories__historic legends_COMPRESSED.pdf.pdf — IX #5 0.1196 · T2 none/none
  - “I The first whites to visit the Owens Valley were basically prospectors looking for gold or other minerals. However, as the mining fever declined amongst some of the visi…”
- [ ] owensvalleyhistory/stories__plea_for_help.pdf.pdf — IX #7 0.0972 · T2 none/none
  - “A Plea for Help Driving some 600 head of cattle and 50 horses, Samuel Addison Bishop, his wife, and several hired hands arrived in the Owens Valley on August 22, 1861 fro…”
- [ ] owensvalleyhistory/stories__southern_inyo.pdf.pdf — IX #12 0.0354 · T2 none/none
  - “ Colorado, which had connected the Owens Valley communities to Keeler and Laws for many years, suspended operations. The tracks and ties were all hauled away. The lonesom…”
- [x] none

## 15. Describe Owens Valley Paiute religion.

- [x] ethnography-of-owens-valley-paiute.pdf — IX #2 0.9957 · KW #3 p114 · T1 academic/mild
  - “Steward: Ethnography of Owen8 Valley Paiute LITERATURE CITED ALDRICH, J. M. 1912. The Biology of Some Western Species of the Dipterous Genus Ephydra. New York Entomologic…”
- [x] owensvalleyhistory/bishop_residents2__page48cc.html.txt — IX #4 0.9884 · KW #2 · T2 none/none
  - “Owens Valley Shoshone - Paiutes Owens Valley Paiute - Bishop, CA Owens Valley Shoshone - Paiutes Bishop - 5 Joe Bowers - Owens Valley Paiute (Courtesy J.D. Blac…”
- [x] owensvalleyhistory/stories__northern paiutes of california and nevada.pdf.pdf — IX #6 0.9629 · KW #1 p74 · T2 none/none
  - “e organization . Moony, James Local History The Ghost Dance Religion, Report Bureau American Ethnology, No. 14 , Pt . 2 , 1896 Chalfant, Guy The Story of Inyo. 1922, priv…”
- [x] payahuunadu-oviwc.pdf — IX #1 0.9983 · KW #7 p1 · T1 primary_indigenous/none
  - “PAYAHUUNADÜ — Owens Valley Indian Water Commission Nüümü (Owens Valley Paiute). A people intricately and intimately tied to water (paya). PAYAHUUNADÜ — Owens Valley India…”
- [ ] water-land-history-oviwc.pdf — IX #9 0.8533 · KW #5 p2 · T1 primary_indigenous/none
  - “ons and diversions on reservation environments the Big Pine Paiute Tribe of the Owens Valley, Bishop Paiute Tribe, Lone Pine Paiute-Shoshone Reservation, and Utu Utu Gwai…”
- [ ] owens-valley-paiute-autobiographies.pdf — IX #10 0.8518 · KW #9 p3 · T1 academic/mild
  - “PANATUBUr, AN OWENS VALLEY PAIUTE By Julian H. Steward Introduction In 1934 the writer supplemented an earlier ethnographic sketch of the Northern Paiute * of Owens Valle…”
- [ ] owensvalleyhistory/independence__page69.html.txt — IX #8 0.9204 · T2 none/none
  - “Pack Train heading up Kearsarge Pass Pack Train heading up Kearsarge Pass Snow covered Onion Valley Road Owens Valley - 1931 Snow covered Onion Valley Road Owens Valley -…”
- [ ] owensvalleyhistory/stories__japanese emperor system as a national religion.pdf.pdf — KW #4 p3 · T2 none/none
  - “KURIHARA: Emperor System as National Religion 317 The second tendency pointed out by Tosaka was the rising tide of New Religions and folk religions. Examples of New Relig…”
- [ ] california-geography-ch12-great-basin.pdf — KW #6 p11 · T3 academic/none
  - “s western neighbors, the Yokuts, who however designated the Owens Valley Paiutes as the southernmost Northern Paiute band living around Owens and Mono Lakes as monachie/m…”
- [ ] ov-native-water-story.pdf — IX #12 0.822 · T1 primary_indigenous/none
  - “Payahǖǖnadǖ Water Story – Wading Through the Past Teri Red Owl This is our water story of Payahǖǖnadǖ, our homelands. We interpret the name as being the place where water…”
- [ ] none

## 16. What was the name of the train that originally ran through Owens Valley?

- [x] owensvalleyhistory/carson_n_colorado__page51d.html.txt — IX #1 0.9922 · T2 none/none
  - “ locomotive #9 going in for repairs and paint. (Photo and text courtesy of Dennis Burke) Southern Pacific Engine No. 2758 at Owenyo (E-Bay auction item) Engine No. 9 paus…”
- [x] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — IX #2 0.9651 · T2 none/none
  - “ the benefits of irrigation. But irrigation demanded water already on the ground, not waiting for it to fall from the sky. Meanwhile, some 250 miles to the north, another…”
- [x] owensvalleyhistory/carson_n_colorado__page51a.html.txt — IX #3 0.9646 · T2 none/none
  - “) The "Slim Princess" #18 in Owens Valley (Photo courtesy of Dennis Burke) SPNG #11 (Photo courtesy of Dennis Burke) The "Slim Princess" in Owens Valley (Photo courtesy o…”
- [ ] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — KW #1 p41 · T2 none/none
  - “POINTS OF INTEREST IN THE OWENS RIVER VALLEY 36 Laws was the name of a stop on the old railroad, and though the railroad is gone, the stop is now a railroad museum. The r…”
- [ ] owensvalleyhistory/california_sierras_trip__dorr_mt whitney trip.pdf.pdf — KW #2 p6 · T2 none/none
  - “inted me interested me as well. I went straight out to San Francisco stayed there for three or four days, seeing some of the Berkeley College men to who I had letters and…”
- [ ] owensvalleyhistory/stories__narrow_gauge_wilderness.pdf.pdf — IX #4 0.9598 · T2 none/none
  - “ the line traversed the Schurz Indian reservation. This resulted in an agreement to haul our original Americans for free. Like many of the early "benefits" bestowed upon …”
- [ ] owensvalleyhistory/stories__A Trip Through the California Sierras_new_REDUCED.pdf.pdf — KW #3 p6 · T2 none/none
  - “inted me interested me as well. I went straight out to San Francisco stayed there for three or four days, seeing some of the Berkeley College men to who I had letters and…”
- [ ] owensvalleyhistory/stories__chronological_history_ov.pdf.pdf — IX #5 0.9595 · T2 none/none
  - “ was in Robber's Roost, robbed stages and freight wagons along the eastern Sierra, especially near Coyote Wells (Freeman Junction) until he was captured later that year. …”
- [ ] owensvalleyhistory/stories__A%20Trip%20Through%20the%20California%20Sierras_new_REDUCED.pdf.pdf — KW #4 p6 · T2 none/none
  - “inted me interested me as well. I went straight out to San Francisco stayed there for three or four days, seeing some of the Berkeley College men to who I had letters and…”
- [ ] owensvalleyhistory/stories__slim_princess.pdf.pdf — IX #6 0.9391 · T2 none/none
  - “ and shipped to Virginia City by camels that had been imported from Africa. Despite Smith's failure with the Columbus operations, he later went on to greater glories in t…”
- [ ] owensvalleyhistory/sierra_names1__page64.html.txt — KW #5 · T2 none/none
  - “Sierra Nevada and Owens Valley Place Names: G - M Sierra Nevada & Owens Valley Place Names: G - M Sequoia National Forest & Sierra National Forest maps courtesy of Greg F…”
- [ ] owensvalleyhistory/stories__some early history of owens river valley.pdf.pdf — KW #6 p3 · T2 none/none
  - “ng the discoveries made, says : "To one of the lakes I gave Owens* name." He gave the names of several of his band to rivers, creeks and lakes that the expedition discove…”
- [ ] owensvalleyhistory/carson_n_colorado__page51f.html.txt — IX #9 0.8746 · T2 none/none
  - “ to a severe cloudburst washing out the tracks - 1920s SP train depot at Owenyo, CA - 1948 Owens Lake during the Cerro Gordo mining days - circa 1880s The Molly Stevens s…”
- [ ] owensvalleyhistory/carson_n_colorado__page51g.html.txt — IX #11 0.8594 · T2 none/none
  - “ the great basin and over-shadowed the queen of the Comstock herself, Virginia City. Ore from , Candelaria and Tonopah rolled over the Carson & Colorado, but never to the…”
- [ ] none

## 17. What counties did the slim princess run through?

- [x] owensvalleyhistory/stories__gleichman_slim_princess_1969.pdf.pdf — IX #1 0.9606 · KW #5 p1 · T2 none/none
  - “1 Sierra Siesta for a Slim Princess By Joan Gleichman Desert Magazine – July 1969 Old Hawthorne No. 61 pulling several cars along the Carson & Colorado, stops at the Cali…”
- [x] owensvalleyhistory/carson_n_colorado__page51i.html.txt — IX #3 0.8029 · KW #6 · T2 none/none
  - “up of narrow gauge rail aficionados in the late 1950s. The "Slim Princess" making a final run from Laws to Owenyo loaded with SPNG fans. [Photo from ] by Gary Speck by Ga…”
- [x] owensvalleyhistory/stories__slim_princess.pdf.pdf — IX #5 0.5652 · KW #10 p5 · T2 none/none
  - “Slim Princess Page 5 of 5 So, as the century ended, the Carson & Colorado Railway continued to struggle through the desert - illogical, improbable, ill-conceive…”
- [ ] owensvalleyhistory/carson_n_colorado__page51b.html.txt — IX #9 0.2844 · KW #1 · T2 none/none
  - “courtesy of Ray DeLea) Heading south at Laws Station. The "Slim Princess" at Aberdeen Crossing - 1946 (Photo courtesy of Dennis Burke) Returning from Zurich station with …”
- [ ] owensvalleyhistory/stories__behind_wofw.pdf.pdf — IX #2 0.8427 · T2 none/none
  - “ posing and passing of the gourd for photographic purposes. He told the newsreel men that they were "making a damfool out of him" and that "all the boys are laughin' at m…”
- [ ] owensvalleyhistory/carson_n_colorado__page51e.html.txt — KW #2 · T2 none/none
  - “do Railroad Crossing the Owens River Laws, CA turntable The Slim Princess at Owenyo The Slim Princess at Kearsarge Station The Slim Princess at the Owenyo transfer trestl…”
- [ ] owensvalleyhistory/carson_n_colorado__page51d.html.txt — KW #3 · T2 none/none
  - “ng on water. (Drawing by Carl Fallberg) Owenyo Station. The Slim Princess on a busy day. (Drawing by Carl Fallberg) (Drawing by Carl Fallberg) (Drawing by Carl Fallberg) …”
- [ ] owensvalleyhistory/carson_n_colorado__page51g.html.txt — KW #4 · T2 none/none
  - “k Datin sketch Engine No. 18 steaming along in Owens Valley Slim Princess #9 steaming through Owens Valley (Photo courtesy Rick Olson) The Slim Princess in action in Owen…”
- [ ] owensvalleyhistory/stories__north_of_bishop.pdf.pdf — IX #4 0.6546 · T2 none/none
  - “ told in a number of fine volumes. In The Slim Princess, a paperback by John Hungerford, the author relates an anecdote about building the line: No sketch of the Carson a…”
- [ ] owensvalleyhistory/laws__page103.html.txt — IX #7 0.4587 · T2 none/none
  - “8. The The Slim Princess The Slim Princess, the last of the Western Narrow Gauge, started out as the . The C & C was a step-child of the Virginia & Truckee RR with its no…”
- [ ] owensvalleyhistory/stories__narrow_gauge_wilderness.pdf.pdf — IX #8 0.3384 · T2 none/none
  - “ a rail extension other than a very costly circuitous route around the mountains. The first bucket of salt was discharged at the new terminus at "Tramway" on July 2, 1913…”
- [ ] none

## 18. When was the slim princess built?

- [x] owensvalleyhistory/stories__gleichman_slim_princess_1969.pdf.pdf — IX #2 0.9971 · KW #1 p1 · T2 none/none
  - “1 Sierra Siesta for a Slim Princess By Joan Gleichman Desert Magazine – July 1969 Old Hawthorne No. 61 pulling several cars along the Carson & Colorado, stops at the Cali…”
- [x] owensvalleyhistory/laws__page103.html.txt — IX #3 0.9965 · KW #3 · T2 none/none
  - “near Bishop, CA. Carson & Colorado RR Locomotive No. 9 The Slim Princess and a string of cars at the Laws Station building and surrounding railroad installations form the…”
- [x] owensvalleyhistory/carson_n_colorado__page51g.html.txt — IX #4 0.9964 · KW #4 · T2 none/none
  - “k Datin sketch Engine No. 18 steaming along in Owens Valley Slim Princess #9 steaming through Owens Valley (Photo courtesy Rick Olson) The Slim Princess in action in Owen…”
- [x] owensvalleyhistory/stories__slim_princess.pdf.pdf — IX #1 0.9977 · KW #10 p5 · T2 none/none
  - “Slim Princess Page 5 of 5 So, as the century ended, the Carson & Colorado Railway continued to struggle through the desert - illogical, improbable, ill-conceive…”
- [ ] owensvalleyhistory/carson_n_colorado__page51b.html.txt — IX #10 0.9885 · KW #2 · T2 none/none
  - “courtesy of Ray DeLea) Heading south at Laws Station. The "Slim Princess" at Aberdeen Crossing - 1946 (Photo courtesy of Dennis Burke) Returning from Zurich station with …”
- [ ] owensvalleyhistory/carson_n_colorado__page51a.html.txt — IX #8 0.9905 · KW #7 · T2 none/none
  - “tted with a snow plow (Photo courtesy of Dennis Burke) The "Slim Princess" #18 in Owens Valley (Photo courtesy of Dennis Burke) SPNG #11 (Photo courtesy of Dennis Burke) …”
- [ ] owensvalleyhistory/carson_n_colorado__page51e.html.txt — IX #12 0.9874 · KW #6 · T2 none/none
  - “do Railroad Crossing the Owens River Laws, CA turntable The Slim Princess at Owenyo The Slim Princess at Kearsarge Station The Slim Princess at the Owenyo transfer trestl…”
- [ ] owensvalleyhistory/carson_n_colorado__page51c.html.txt — IX #6 0.9944 · T2 none/none
  - “1954 Richard C. Dayton (left) along one of the many models he made for the movie industry. This is the day he took the Enterprise model to Desilu Studios. In case you are…”
- [ ] owensvalleyhistory/carson_n_colorado__page51d.html.txt — KW #5 · T2 none/none
  - “ng on water. (Drawing by Carl Fallberg) Owenyo Station. The Slim Princess on a busy day. (Drawing by Carl Fallberg) (Drawing by Carl Fallberg) (Drawing by Carl Fallberg) …”
- [ ] owensvalleyhistory/stories__narrow_gauge_wilderness.pdf.pdf — IX #9 0.9893 · T2 none/none
  - “ a rail extension other than a very costly circuitous route around the mountains. The first bucket of salt was discharged at the new terminus at "Tramway" on July 2, 1913…”
- [ ] none

## 19. What kind of train was the slim princess?

- [x] owensvalleyhistory/stories__gleichman_slim_princess_1969.pdf.pdf — IX #1 0.991 · KW #1 p1 · T2 none/none
  - “1 Sierra Siesta for a Slim Princess By Joan Gleichman Desert Magazine – July 1969 Old Hawthorne No. 61 pulling several cars along the Carson & Colorado, stops at the Cali…”
- [x] owensvalleyhistory/laws__page103.html.txt — IX #2 0.984 · KW #4 · T2 none/none
  - “near Bishop, CA. Carson & Colorado RR Locomotive No. 9 The Slim Princess and a string of cars at the Laws Station building and surrounding railroad installations form the…”
- [x] owensvalleyhistory/carson_n_colorado__page51a.html.txt — IX #5 0.9729 · KW #2 · T2 none/none
  - “tted with a snow plow (Photo courtesy of Dennis Burke) The "Slim Princess" #18 in Owens Valley (Photo courtesy of Dennis Burke) SPNG #11 (Photo courtesy of Dennis Burke) …”
- [x] owensvalleyhistory/carson_n_colorado__page51g.html.txt — IX #3 0.9819 · KW #5 · T2 none/none
  - “k Datin sketch Engine No. 18 steaming along in Owens Valley Slim Princess #9 steaming through Owens Valley (Photo courtesy Rick Olson) The Slim Princess in action in Owen…”
- [ ] owensvalleyhistory/carson_n_colorado__page51e.html.txt — IX #6 0.9684 · KW #7 · T2 none/none
  - “do Railroad Crossing the Owens River Laws, CA turntable The Slim Princess at Owenyo The Slim Princess at Kearsarge Station The Slim Princess at the Owenyo transfer trestl…”
- [ ] owensvalleyhistory/carson_n_colorado__page51h.html.txt — IX #4 0.98 · T2 none/none
  - “SPNG - Keeler, Owens Lake Southern Pacific Narrow Gauge Railroad Keeler Cerro Gordo Bowland Owens Lake All material courtesy of Rich McCutchan unless otherwise noted. See…”
- [ ] owensvalleyhistory/carson_n_colorado__page51b.html.txt — KW #3 · T2 none/none
  - “courtesy of Ray DeLea) Heading south at Laws Station. The "Slim Princess" at Aberdeen Crossing - 1946 (Photo courtesy of Dennis Burke) Returning from Zurich station with …”
- [ ] owensvalleyhistory/stories__north_of_bishop.pdf.pdf — IX #11 0.9528 · KW #10 p1 · T2 none/none
  - “and Colorado it was and its affectionate nickname was "The Slim Princess," because it had a kind of regal sagebrushy charm. It chugged through Dayton, Wabuska, Schurz, Gi…”
- [ ] owensvalleyhistory/carson_n_colorado__page51c.html.txt — IX #8 0.9644 · T2 none/none
  - “1954 Richard C. Dayton (left) along one of the many models he made for the movie industry. This is the day he took the Enterprise model to Desilu Studios. In case you are…”
- [ ] owensvalleyhistory/carson_n_colorado__page51d.html.txt — KW #6 · T2 none/none
  - “ng on water. (Drawing by Carl Fallberg) Owenyo Station. The Slim Princess on a busy day. (Drawing by Carl Fallberg) (Drawing by Carl Fallberg) (Drawing by Carl Fallberg) …”
- [ ] none

## 20. How did the Owens Valley locals retaliate against the aqueduct in the years following the finished project?

- [x] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #3 0.908 · KW #7 p3 · T2 none/none
  - “PROFIT The San Fernando Valley lies just north of Los Angeles. Both the coast line and the valley line of the Southern Pacific Railroad cross it. Twenty years ago the San…”
- [x] owensvalleyhistory/stories__aqueduct_history.pdf.pdf — IX #8 0.6494 · KW #3 p1 · T2 none/none
  - “1 L. A. AQUEDUCT HISTORY IS TOLD Here is the eighth of a series of dramatic fact stories of the tragedy that has overtaken the Owens River Valley in Inyo County, where…”
- [x] owensvalleyhistory/ov_aqueduct__page20c.html.txt — IX #1 0.9665 · T2 none/none
  - “Los Angeles Aqueduct - Valley Rebellion Owens Valley's - Los Angeles Aqueduct If I am not on the JOB, You can find me at the AQUEDUCT was the rallying cry for the people …”
- [x] owensvalleyhistory/stories__police_ready.pdf.pdf — IX #2 0.9574 · T2 none/none
  - “ that has been conducted against this city and its Department of Water and Power for more than three years. From the beginning this campaign has been characterized by fla…”
- [ ] owensvalleyhistory/ov_aqueduct__page20.html.txt — KW #1 · T2 none/none
  - “Los Angeles Aqueduct - Olancha Owens Valley's - Los Angeles Aqueduct Unless otherwise note, All L.A. aqueduct photographs on these pages are from the unless otherwise not…”
- [ ] owensvalleyhistory/stories__Los_Angeles_Department_of_Water_and_Power_Operations_in_the_Mono_Basin.pdf.pdf — KW #2 p3 · T2 none/none
  - “-3- MONO BASIN PROJECT BENEFITS CONSTRUCTION OF THE MONO BASIN PROJECT HAS RESULTED IN THE FOLLOWING SIGNIFICANT BENEFITS: 1, MONO BASIN DIVERSIONS PROVIDE NEARLY 20 PERC…”
- [ ] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — IX #5 0.8046 · T2 none/none
  - “ had expressed an interest in connecting Los Angeles to the Owens River by way of an aqueduct that would stretch some 235 miles from the valley to the city, an idea first…”
- [ ] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — KW #4 p7 · T2 none/none
  - “n preliminary anyway, withdrew its plans for a contemplated Owens Valley reclamation project. Angry Owens Valley residents branded Lippincott as "Judas B. Lippincott." Li…”
- [ ] owensvalleyhistory/ov_aqueduct__page20a.html.txt — KW #5 · T2 none/none
  - “e opened on September 14, and that on that date and the two following days the inauguration of traffic operations between the two minlng towns will be fittingly celebrate…”
- [ ] owensvalleyhistory/stories__owens_lake_land_use_REDUCED.pdf.pdf — KW #6 p7 · T2 none/none
  - “the proposed project area as Natural Resources and State and Federal Lands.29 Lands adjacent to the lake bed are primarily flat, desert open space with sparse vegetation.…”
- [ ] owensvalleyhistory/stories__never_the_same.pdf.pdf — IX #7 0.6924 · T2 none/none
  - “Things Will Never Quite be the Same The City of Los Angeles quickly and quietly began the process of acquiring water rights through permits, condemnations and outright la…”
- [ ] owensvalleyhistory/ghosts_of_past2__page9.html.txt — IX #9 0.4493 · T2 none/none
  - “ to fishing because of severe poaching, and giardia was introduced to the streams of the area. What a terrible price to pay for a road to nowhere. Sherman Stevens Sawmill…”
- [ ] owensvalleyhistory/ov_aqueduct__page20b.html.txt — IX #12 0.3514 · T2 none/none
  - “Los Angeles Aqueduct - Desert and City Owens Valley's - Los Angeles Aqueduct Unless otherwise note, All L.A. aqueduct photographs on these pages are from the unless other…”
- [ ] none

## 21. Describe how the white settlers and native paiutes got along in Owens Valley in the years after the aqueduct was built.

- [x] owensvalleyhistory/stories__time_changes.pdf.pdf — IX #4 0.9076 · KW #2 · T2 none/none
  - “es Change for Everyone It's estimated that as many as 2,000 Native Americans called Inyo and the Eastern Sierra home when white European settlers first arrived m the mid …”
- [x] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #2 0.9715 · KW #6 p2 · T2 none/none
  - “len Matlick History Page 2 There were Paiute Indians living along the Owens River and Bishop Creek. They were a friendly people and few incidents of friction occurred bet…”
- [x] owensvalleyhistory/stories__historic legends_COMPRESSED.pdf.pdf — IX #6 0.8382 · KW #5 p21 · T2 none/none
  - “ependence was continually garrisoned. With the army back in Owens Valley, most of the remaining Paiutes resumed their peaceful ways. A handful, however, never were able t…”
- [x] water-land-history-oviwc.pdf — IX #1 0.9857 · T1 primary_indigenous/none
  - “WATER & LAND HISTORY — Owens Valley Indian Water Commission A HISTORY OF WATER RIGHTS & LAND STRUGGLES Time Immemorial The Nüümü have lived in Payahuunadü “Land of the Fl…”
- [ ] owensvalleyhistory/stories__plea_for_help.pdf.pdf — KW #1 · T2 none/none
  - “on Bishop, his wife, and several hired hands arrived in the Owens Valley on August 22, 1861 from Fort Tejon in the Tehachapi Mountains. Bishop and his wife were some of t…”
- [ ] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #3 0.9101 · T2 none/none
  - “1 STRUGGLE FOR WATER IN OWENS VALLEY IS TOLD BY CALL STAFF WRITER Here is the second of a series of dramatic fact stories of the tragedy that has overtaken the Owens Rive…”
- [ ] owensvalleyhistory/stories__chronological_history_ov.pdf.pdf — IX #9 0.7763 · KW #7 p2 · T2 none/none
  - “Chronological History of Owens Valley Page 2 of 6 1849 The Jayhawkers passed through our area on their way to the gold fields of the Western Sierras. 1849 The Bennett and…”
- [ ] california-geography-ch5-water.pdf — KW #3 p11 · T3 academic/none
  - “d to raise cattle on the luxuriant grasses that grew in the Owens Valley. The ranchers came into conflict with the Paiutes over land and water use, and most of the Paiute…”
- [ ] owensvalleyhistory/bishop_residents2__page48cc.html.txt — KW #4 · T2 none/none
  - “Owens Valley Shoshone - Paiutes Owens Valley Paiute - Bishop, CA Owens Valley Shoshone - Paiutes Bishop - 5 Joe Bowers - Owens Valley Paiute (Courtesy J.D. Blac…”
- [ ] ov-native-water-story.pdf — IX #5 0.8401 · T1 primary_indigenous/none
  - “ M. von Schmidt’s 1855-56 survey of the Owens Valley for the federal government. As part of his report for the state, he created this map which shows the irrigated areas …”
- [ ] ethnography-of-owens-valley-paiute.pdf — IX #7 0.8079 · T1 academic/mild
  - “ Tom Stone (Bish.), plate lc, about 40 years old, very communicative and with an extraordinary memory for old customs described by his-grandfather; S.N., Sam Newland (Bis…”
- [ ] none

## 22. Describe the chemical makeup of Owens Lake before the aqueduct diverted its water.

- [x] owensvalleyhistory/stories__a_lake_no_more.pdf.pdf — IX #1 0.983 · KW #3 p1 · T2 none/none
  - “1 A Lake No More Before diversions began, Owens Lake covered over 100 square miles of the Owens Valley floor. Steamships had once plied its water carrying silver bu…”
- [x] owensvalleyhistory/stories__armstrong_why_owens_lake_is_red_1981.pdf.pdf — IX #2 0.9011 · KW #7 p1 · T2 none/none
  - “Why Owens Lake is Red By Wayne P. Armstrong Desert Magazine – May 1981 One of nature's most remarkable biological phenomena is the pink and red coloration of salt l…”
- [x] geology-and-water-resources-ov-report.pdf — IX #4 0.4135 · KW #1 p60 · T3 institutional_bias/mild
  - “In the Owens Lake Basin, the streams are diverted into the Los Angeles Aqueduct about 2 mi west of the natural channel of the lower Owens River. The combined waters of…”
- [x] owensvalleyhistory/owens_valley_owens_lake__page99.html.txt — IX #3 0.6958 · KW #6 · T2 none/none
  - “M.D. on the occasion of the construction of the Los Angeles Aqueduct Owens Lake near the middle - 1909 Photos of Owens Lake from wet winters Owens Lake - August 1969 (Pho…”
- [ ] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — KW #2 p56 · T2 none/none
  - “51 POINTS OF INTEREST IN THE OWENS RIVER VALLEY Approximately 350 miles from Los Angeles, Mono Lake marks the last visible effects of the Los Angeles Aqueduct system. Alt…”
- [ ] california-geography-ch5-water.pdf — KW #4 p13 · T3 academic/none
  - “lliam Mulholland Addressing the Crowd at the Opening of the Aqueduct. Image by Los Angeles Department of Water and Power is in the public domain. After the aqueduct was c…”
- [ ] owensvalleyhistory/stories__soda_ash_industry.pdf.pdf — KW #5 p17 · T2 none/none
  - “eelbarrows to haul it to the plant. By 1914, the demand for water in Los Angeles and other cities required the construction of the Los Angeles aqueduct, which diverted wa…”
- [ ] owensvalleyhistory/stories__death valley men_COMPRESSED.pdf.pdf — IX #6 0.1981 · T2 none/none
  - “ Lake. The chemical plants extract soda and allied salts from the thick saline solution which is Owens Lake. The lake is unbeautiful and the soda works, through which the…”
- [ ] owensvalleyhistory/stories__some early history of owens river valley.pdf.pdf — IX #8 0.1116 · T2 none/none
  - “ at any one other spot on i borders. "This lake is emphatically a "saline lake," as its waters contain salts to near the point of saturation, producing a density sufficie…”
- [ ] owensvalleyhistory/stories__police_ready.pdf.pdf — IX #13 0.0589 · T2 none/none
  - “ that has been conducted against this city and its Department of Water and Power for more than three years. From the beginning this campaign has been characterized by fla…”
- [ ] owensvalleyhistory/ghosts_of_past2__page9.html.txt — IX #14 0.0392 · T2 none/none
  - “ to fishing because of severe poaching, and giardia was introduced to the streams of the area. What a terrible price to pay for a road to nowhere. Sherman Stevens Sawmill…”
- [ ] none

## 23. Was Owens Valley a desert before the aqueduct diverted the water?

- [x] owensvalleyhistory/stories__a_lake_no_more.pdf.pdf — IX #2 0.996 · KW #3 p1 · T2 none/none
  - “1 A Lake No More Before diversions began, Owens Lake covered over 100 square miles of the Owens Valley floor. Steamships had once plied its water carrying silver bullion …”
- [x] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #1 0.997 · KW #7 p4 · T2 none/none
  - “Valley of Broken Hearts – Part 2 4 They will even remind you, if the thought had not occurred to you, that for every acre brought under cultivation about the to…”
- [x] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — IX #4 0.985 · KW #4 p56 · T2 none/none
  - “51 POINTS OF INTEREST IN THE OWENS RIVER VALLEY Approximately 350 miles from Los Angeles, Mono Lake marks the last visible effects of the Los Angeles Aqueduct system. Alt…”
- [x] owensvalleyhistory/stories__aqueduct_history.pdf.pdf — IX #3 0.9894 · T2 none/none
  - “1 L. A. AQUEDUCT HISTORY IS TOLD Here is the eighth of a series of dramatic fact stories of the tragedy that has overtaken the Owens River Valley in Inyo County, where al…”
- [ ] california-geography-ch5-water.pdf — KW #1 p13 · T3 academic/none
  - “lliam Mulholland Addressing the Crowd at the Opening of the Aqueduct. Image by Los Angeles Department of Water and Power is in the public domain. After the aqueduct was c…”
- [ ] geology-and-water-resources-ov-report.pdf — KW #2 p60 · T3 institutional_bias/mild
  - “In the Owens Lake Basin, the streams are diverted into the Los Angeles Aqueduct about 2 mi west of the natural channel of the lower Owens River. The combined waters of…”
- [ ] owensvalleyhistory/el_camino_sierra_tales__page111.html.txt — IX #5 0.9849 · T2 none/none
  - “ Valley into an agricultural super farm. The committee saw the abundant water in the streams from the Sierra Nevada (this was pre L.A. diversions) and concluded the use o…”
- [ ] owensvalleyhistory/ov_aqueduct__page18.html.txt — IX #9 0.956 · KW #10 · T2 none/none
  - “more or less indefinite, for the rreason that the water companies do not all use the same head above the center of the aperture, and the inch varies from 1.36 to 1.73 cub…”
- [ ] owensvalleyhistory/stories__police_ready.pdf.pdf — IX #6 0.9805 · T2 none/none
  - “ that has been conducted against this city and its Department of Water and Power for more than three years. From the beginning this campaign has been characterized by fla…”
- [ ] owensvalleyhistory/ov_aqueduct__page20b.html.txt — KW #5 · T2 none/none
  - “e Photo from the 1916 book "Construction of the Los Angeles Aqueduct Final Report " by the Board of Public Service Commissioners of the City of Los Angeles. Hauling freig…”
- [ ] owensvalleyhistory/stories__some early history of owens river valley.pdf.pdf — IX #7 0.9703 · T2 none/none
  - “ in regard to the man for whom the river was named. He replied : "The resources of the city library have been exhausted, but nothing has been found to give the desired in…”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — KW #6 p4 · T2 none/none
  - “ey did not sell-out to Los Angeles when the city bought the water rights in Mono and Inyo counties. Al originally paid $10 an acre for his ranch and, in 1930, was quoted …”
- [ ] none

## 24. Who was William Mulholland and what was his role in the Los Angeles Aqueduct project?

- [x] owensvalleyhistory/ov_aqueduct__mulholland1.html.txt — IX #1 0.9997 · KW #3 · T2 none/none
  - “is exactly what Los Angeles citizens have done. Without the additional water supply delivered by the aqueduct he built, Los Angeles could never have grown beyond the 500,…”
- [x] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — IX #2 0.9969 · KW #2 p6 · T2 none/none
  - “s to bring potential buyers out to the San Fernando Valley. Mulholland knew what was going on but could do little about it; the terminus of the aqueduct was from an en­ g…”
- [x] owensvalleyhistory/ov_aqueduct__page18.html.txt — IX #3 0.9967 · KW #1 · T2 none/none
  - “Lippincott, Fred A. Eaton, and William Mulholland (1906 Los Angeles Times Photo) Los Angeles Board of Water Commissioners at the time of the building of the Los Angeles a…”
- [x] owensvalleyhistory/stories__aqueduct_history.pdf.pdf — IX #4 0.9939 · KW #6 p1 · T2 none/none
  - “1 L. A. AQUEDUCT HISTORY IS TOLD Here is the eighth of a series of dramatic fact stories of the tragedy that has overtaken the Owens River Valley in Inyo County, where…”
- [ ] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — IX #15 0.8468 · KW #5 p7 · T2 none/none
  - “hdrew its plans for a contemplated Owens Valley reclamation project. Angry Owens Valley residents branded Lippincott as "Judas B. Lippincott." Lippincott wrote numerous a…”
- [ ] owensvalleyhistory/stories__An Irishmans Diary about Fr John Crowley.pdf.pdf — IX #9 0.9745 · T2 none/none
  - “ who was educated in O’Connell’s CBS in Dublin, was a key figure behind a plan to divert the Owens River through an 223-mile aqueduct to a nascent and arid Los Angeles. A…”
- [ ] owensvalleyhistory/ov_aqueduct__page20b.html.txt — IX #14 0.8975 · KW #9 · T2 none/none
  - “ns into place Photo from the 1916 book "Construction of the Los Angeles Aqueduct Final Report " by the Board of Public Service Commissioners of the City of Los Angeles. H…”
- [ ] california-geography-ch5-water.pdf — KW #4 p11 · T3 academic/none
  - “er 40,000 grape vines, apple trees and grazing pastures The Los Angeles Aqueduct Frederick Eaton and William Mulholland were two of the more visible principals in the Cal…”
- [ ] owensvalleyhistory/stories__An%20Irishmans%20Diary%20about%20Fr%20John%20Crowley.pdf.pdf — IX #10 0.9745 · T2 none/none
  - “ who was educated in O’Connell’s CBS in Dublin, was a key figure behind a plan to divert the Owens River through an 223-mile aqueduct to a nascent and arid Los Angeles. A…”
- [ ] owensvalleyhistory/stories__aqueduct_excursion.pdf.pdf — IX #13 0.9005 · T2 none/none
  - “ here to supply electric light, compressed air and water for work in the five-mile tunnel. A trolley line operates from the mouth of the tunnel to dispose of the waste. R…”
- [ ] none

## 25. What was the Saint Francis Dam disaster and how did it affect public trust in the Los Angeles Department of Water and Power?

- [x] california-geography-ch5-water.pdf — KW #1 p15 · T3 academic/none
  - “Figure 5.9: The Aftermath of the St. Francis Dam Collapse, 1928. Image by Los Angeles Department of Water and Power is in the public domain. The consequences of the dam f…”
- [ ] owensvalleyhistory/stories__hydro electric developmens in southern ca.pdf.pdf — KW #2 p9 · T2 none/none
  - “ornia Electric Corporation . . . 43 Beginnings of the Super-power system ........... 45 Hydro generation and World War I ............. 47 Edison absorbs Mount Whitney Pow…”
- [ ] owensvalleyhistory/ov_aqueduct__page18.html.txt — IX #7 0.0124 · KW #3 · T2 none/none
  - “, and the adjacent Colorado River states. "When Rome falls (Los Angeles and its unquenchable thirst for water) there will be such a shout of freedom that the world will n…”
- [ ] owensvalleyhistory/stories__An Irishmans Diary about Fr John Crowley.pdf.pdf — IX #1 0.134 · KW #5 p2 · T2 none/none
  - “into a force for change. The Los Angeles authorities eventually gave way to a limited extent, allowing a dam and a vast reservoir to be built at the top of the valley, wh…”
- [ ] ov-native-water-story.pdf — IX #4 0.0511 · KW #4 p2 · T1 primary_indigenous/none
  - “Commission. Instead, in 1930, Los Angeles produced a report that said those lands were “non-operative waste land” and they should be removed from trust status and made pu…”
- [ ] owensvalleyhistory/stories__An%20Irishmans%20Diary%20about%20Fr%20John%20Crowley.pdf.pdf — IX #2 0.134 · KW #6 p2 · T2 none/none
  - “into a force for change. The Los Angeles authorities eventually gave way to a limited extent, allowing a dam and a vast reservoir to be built at the top of the valley, wh…”
- [ ] owensvalleyhistory/stories__the_gridiron_civil war threatened.pdf.pdf — IX #3 0.0974 · T2 none/none
  - “ their names are as follows: Isaac Joes, Orange County; Bradford S. Crittenden of Tracy; T. M. Wright of Santa Clara; Elbert G. Adams of Merced; Frank W. Mixter of Tulare…”
- [ ] owensvalleyhistory/stories__police_ready.pdf.pdf — IX #5 0.0404 · T2 none/none
  - “1 POLICE READY TO RUSH NORTH Armed Men Prepared for New Aqueduct Trouble Investigation by Grand Jury May be Requested State Senator Swing Offers Aid to End Feud Los Angel…”
- [ ] owensvalleyhistory/stories__Los_Angeles_Department_of_Water_and_Power_Operations_in_the_Mono_Basin.pdf.pdf — IX #6 0.0129 · T2 none/none
  - “LOS ANGELES DEPARTMENT OF WATER AND POWER OPERATIONS IN THE MONO BASIN* I APPRECIATE THIS OPPORTUNITY TO COMMENT ON THE DEPARTMENT'S WATER GATHERING OPERATIONS IN THE MON…”
- [ ] owensvalleyhistory/stories__owens_valley_facts_printed.pdf.pdf — IX #8 0.0112 · T2 none/none
  - “ seemed strong in favor of the people of Owens Valley.” “This publicity has hurt Los Angeles terribly. Los Angeles, with her billions of dollars of invested capital, cann…”
- [ ] none

## 26. Describe the Paiute people's relationship with water and land in Owens Valley before white settlement.

- [x] water-land-history-oviwc.pdf — IX #2 0.9998 · KW #1 p3 · T1 primary_indigenous/none
  - “fied by all of the Tribes because it lacked access to “wet” water, infrastructure funding, land acquisition, and the usual benefits found in water settlements. The agreem…”
- [x] payahuunadu-oviwc.pdf — IX #1 1.0 · KW #3 p3 · T1 primary_indigenous/none
  - “Our Ecology Prior to Western Contact The Nüümü (Owens Valley Paiute) are a people born of water. Our oral histories, passed down from generation to generation, tell of th…”
- [x] ov-native-water-story.pdf — IX #3 0.9991 · KW #2 p2 · T1 primary_indigenous/none
  - “the region, costs of facilities to serve water for both agricultural and non-agricultural water demands, and the economic returns to justify the claims of water. In July …”
- [x] ethnography-of-owens-valley-paiute.pdf — IX #4 0.997 · KW #5 p9 · T1 academic/mild
  - “Steward: Ethnography of Owen8s Valley Paiute TRIBAL DISTRIBUTIONS The Owens Valley Paiute are the southernmost of that widely dis- tributed Shoshonean group, the Northern…”
- [ ] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — IX #11 0.9649 · KW #8 p4 · T2 none/none
  - “The Owens River Valley is the subject of this guidebook published by the Center for Land Use Interpretation, one of a series of occasional regional titles produced…”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #9 0.985 · T2 none/none
  - “ordo Freighting company, based in Mojave, California. His travels took him through Bishop in the beautiful Owens Valley. It captivated Al from the moment he first saw it.…”
- [ ] california-geography-ch5-water.pdf — KW #4 p11 · T3 academic/none
  - “d to raise cattle on the luxuriant grasses that grew in the Owens Valley. The ranchers came into conflict with the Paiutes over land and water use, and most of the Paiute…”
- [ ] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #10 0.9697 · T2 none/none
  - “1 STRUGGLE FOR WATER IN OWENS VALLEY IS TOLD BY CALL STAFF WRITER Here is the second of a series of dramatic fact stories of the tragedy that has overtaken the Owens Rive…”
- [ ] owensvalleyhistory/stories__board_denies_inyo_liability.pdf.pdf — KW #6 p1 · T2 none/none
  - “1 BOARD DENIES INYO LIABILITY Answers Chamber Proposal on Owens Reparations Long-Standing Offer to Buy Land Withdrawn Conference Plan Accepted, if Authorized Los Angeles …”
- [ ] owensvalleyhistory/independence__page69.html.txt — IX #13 0.9584 · T2 none/none
  - “Pack Train heading up Kearsarge Pass Pack Train heading up Kearsarge Pass Snow covered Onion Valley Road Owens Valley - 1931 Snow covered Onion Valley Road Owens Valley -…”
- [ ] none

## 27. What was the role of Fred Eaton in acquiring Owens Valley land for the Los Angeles Aqueduct?

- [x] water-land-history-oviwc.pdf — IX #1 0.9966 · KW #4 p1 · T1 primary_indigenous/none
  - “WATER & LAND HISTORY — Owens Valley Indian Water Commission A HISTORY OF WATER RIGHTS & LAND STRUGGLES Time Immemorial The Nüümü have lived in Payahuunadü “Land of the…”
- [x] owensvalleyhistory/ov_aqueduct__page18.html.txt — IX #3 0.9955 · KW #2 · T2 none/none
  - “"Ben Hur" might well be heard again in Northern California, Owens Valley, and the adjacent Colorado River states. "When Rome falls (Los Angeles and its unquenchable thirs…”
- [x] owensvalleyhistory/stories__riverside_daily_press.pdf.pdf — IX #4 0.9931 · KW #9 p1 · T2 none/none
  - “1 River#ide Daily Pre## THURSDAY, JULY 7, 1892 The Owens River Valley. (by Fred Eaton) (Article courtesy of Hal Eaton) Fred Eaton of Los Angeles has just returned from an…”
- [x] owensvalleyhistory/ov_aqueduct__page20c.html.txt — IX #12 0.8096 · KW #3 · T2 none/none
  - “Los Angeles Aqueduct - Valley Rebellion Owens Valley's - Los Angeles Aqueduct If I am not on the JOB, You can find me at the AQUEDUCT was the rallying cry for t…”
- [ ] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — IX #9 0.918 · KW #6 p6 · T2 none/none
  - “6 them. In November 1904 Mulholland, Eaton, and Lippincott met with Newell in Los Angeles. Mulholland promised Newell that any project undertaken by Los Angeles would be …”
- [ ] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — IX #2 0.9965 · T2 none/none
  - “ had expressed an interest in connecting Los Angeles to the Owens River by way of an aqueduct that would stretch some 235 miles from the valley to the city, an idea first…”
- [ ] california-geography-ch5-water.pdf — KW #1 p12 · T3 academic/none
  - “on building an irrigation system to help the farmers of the Owens Valley, which would block Los Angeles from diverting the water. From 1902 to 1905, Eaton used underhande…”
- [ ] owensvalleyhistory/stories__greatest_good.pdf.pdf — IX #6 0.9652 · T2 none/none
  - “The Greatest Good for the Greatest Number? Some of the City fathers of Los Angeles were already well aware of possible sources for LA's growing water needs. Fred Eaton wa…”
- [ ] owensvalleyhistory/stories__aqueduct_history.pdf.pdf — IX #7 0.9607 · T2 none/none
  - “ Aqueduct History Told 3 When the construction of the aqueduct began the valley residents assumed, of course, that Mulholland would forthwith provide a real storage reser…”
- [ ] owensvalleyhistory/stories__hydroelectric power history.pdf.pdf — KW #5 p43 · T2 none/none
  - “.be~I1.l!!-.~he first decade of the twentieth century, when Los Angeles' Municipal Water System's chief engineer, William Mulholland, began investigating the Owens River …”
- [ ] owensvalleyhistory/stories__police_ready.pdf.pdf — IX #11 0.8385 · T2 none/none
  - “ Valley. Its tax bill for the present year amounted to $144,000 or 43 percent of the total county taxes. Ever since the Aqueduct was placed in operation, the city of Los …”
- [ ] none

## 28. How did the construction of the Los Angeles Aqueduct affect agriculture in Owens Valley?

- [x] owensvalleyhistory/ov_aqueduct__page20a.html.txt — IX #1 0.9956 · KW #2 · T2 none/none
  - “Los Angeles Aqueduct - Rose Valley Owens Valley's - Los Angeles Aqueduct Unless otherwise note, All L.A. aqueduct photographs on these pages are from the unless…”
- [x] owensvalleyhistory/ov_aqueduct__page19.html.txt — IX #4 0.993 · KW #1 · T2 none/none
  - “ve, all of which will produce anything that can be grown in Los Angeles county, including oranges. It is to be hoped that very soon the railroad, as above proposed, will …”
- [x] owensvalleyhistory/ov_aqueduct__page18.html.txt — IX #2 0.9933 · KW #6 · T2 none/none
  - “"Ben Hur" might well be heard again in Northern California, Owens Valley, and the adjacent Colorado River states. "When Rome falls (Los Angeles and its unquenchable thirs…”
- [x] owensvalleyhistory/ov_aqueduct__page20b.html.txt — IX #6 0.9916 · KW #3 · T2 none/none
  - “Hauling pipe sections into place Photo from the 1916 book "Construction of the Los Angeles Aqueduct Final Report " by the Board of Public Service Commissioners of the Cit…”
- [ ] owensvalleyhistory/stories__chronological_history_ov.pdf.pdf — IX #5 0.9923 · KW #8 p5 · T2 none/none
  - “Chronological History of Owens Valley Page 5 of 6 1908 The Nevada and California Railroad (now Southern Pacific) extended the Owenyo line north from Mojave into the Owens…”
- [ ] owensvalleyhistory/stories__police_ready.pdf.pdf — IX #7 0.9906 · KW #7 p2 · T2 none/none
  - “interests in the valley resulting from the city’s land purchases in that region. In an effort to support their demands for unreasonable land prices and ‘reparations’ this…”
- [ ] owensvalleyhistory/ghosts_of_past2__page9.html.txt — IX #3 0.9933 · T2 none/none
  - “ to fishing because of severe poaching, and giardia was introduced to the streams of the area. What a terrible price to pay for a road to nowhere. Sherman Stevens Sawmill…”
- [ ] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — KW #4 p8 · T2 none/none
  - “vers in the Desert: William Mulholland and the Inventing of Los Ange­ les. New York: HarperCollins, 1993. Department of Public Service of the City of Los Angeles. Complet…”
- [ ] owensvalleyhistory/ov_aqueduct__page20.html.txt — KW #5 · T2 none/none
  - “Los Angeles Aqueduct - Olancha Owens Valley's - Los Angeles Aqueduct Unless otherwise note, All L.A. aqueduct photographs on these pages are from the unless oth…”
- [ ] owensvalleyhistory/ov_aqueduct__page20c.html.txt — IX #8 0.9905 · T2 none/none
  - “Los Angeles Aqueduct - Valley Rebellion Owens Valley's - Los Angeles Aqueduct If I am not on the JOB, You can find me at the AQUEDUCT was the rallying cry for the people …”
- [ ] none

## 29. What happened to Owens Lake after the aqueduct diverted its water, and what environmental consequences followed?

- [x] owensvalleyhistory/stories__a_lake_no_more.pdf.pdf — IX #1 0.997 · KW #5 p1 · T2 none/none
  - “1 A Lake No More Before diversions began, Owens Lake covered over 100 square miles of the Owens Valley floor. Steamships had once plied its water carrying silver bu…”
- [x] geology-and-water-resources-ov-report.pdf — IX #4 0.8041 · KW #3 p60 · T3 institutional_bias/mild
  - “In the Owens Lake Basin, the streams are diverted into the Los Angeles Aqueduct about 2 mi west of the natural channel of the lower Owens River. The combined waters of…”
- [x] owensvalleyhistory/owens_valley_owens_lake__page99.html.txt — IX #2 0.9571 · T2 none/none
  - “ the Los Angeles Aqueduct Owens Lake near the middle - 1909 Photos of Owens Lake from wet winters Owens Lake - August 1969 (Photo courtesy of Ray DeLea) My dad was a chem…”
- [ ] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — KW #1 p6 · T2 none/none
  - “a strong protest against Los Angeles wa­ ter policies. Some Owens Valley residents resorted to violence. Between 1924 and 1927 the aqueduct was dynamited at least a dozen…”
- [ ] california-geography-ch5-water.pdf — KW #2 p13 · T3 academic/none
  - “lliam Mulholland Addressing the Crowd at the Opening of the Aqueduct. Image by Los Angeles Department of Water and Power is in the public domain. After the aqueduct was c…”
- [ ] owensvalleyhistory/ghosts_of_past2__page9.html.txt — IX #3 0.8707 · T2 none/none
  - “ to fishing because of severe poaching, and giardia was introduced to the streams of the area. What a terrible price to pay for a road to nowhere. Sherman Stevens Sawmill…”
- [ ] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — KW #4 p56 · T2 none/none
  - “51 POINTS OF INTEREST IN THE OWENS RIVER VALLEY Approximately 350 miles from Los Angeles, Mono Lake marks the last visible effects of the Los Angeles Aqueduct system. Alt…”
- [ ] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #5 0.767 · T2 none/none
  - “ miles of desert. To the relinquishment of water for Los Angeles domestic use the people of Owens Valley have long since been reconciled. But to the use of this water for…”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — KW #6 p4 · T2 none/none
  - “e’s going to kill a bunch of men! ” She doesn’t recall what happened after that, but Al was successful in dissuading them. The Matlicks were one of the few families that …”
- [ ] owensvalleyhistory/stories__police_ready.pdf.pdf — IX #6 0.6913 · T2 none/none
  - “ that has been conducted against this city and its Department of Water and Power for more than three years. From the beginning this campaign has been characterized by fla…”
- [ ] ov-native-water-story.pdf — IX #7 0.6499 · T1 primary_indigenous/none
  - “. Because they had stolen the rich soils of our homeland, we moved to the sites, we began to make homes in the areas we once lived on and became day laborers for the whit…”
- [ ] owensvalleyhistory/stories__aqueduct_history.pdf.pdf — IX #8 0.5857 · T2 none/none
  - “1 L. A. AQUEDUCT HISTORY IS TOLD Here is the eighth of a series of dramatic fact stories of the tragedy that has overtaken the Owens River Valley in Inyo County, where al…”
- [ ] none

## 30. Describe the economic conditions of Bishop, California in the decades following the aqueduct completion.

- [ ] owensvalleyhistory/stories__time_changes.pdf.pdf — KW #1 · T2 none/none
  - “ved m the mid 1800s. As times changed over the next several decades, so they did for the Native Americans. Water rights retained by the local Paiute-Shoshone were as aggr…”
- [ ] owensvalleyhistory/stories__rediscovering_hockett_trail.pdf.pdf — KW #2 p2 · T2 none/none
  - “by pack trains, the army, and recreationalists for several decades following its completion. The trail was named after the founder, John B. Hockett, in 1863. It was being…”
- [ ] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — KW #3 p6 · T2 none/none
  - “years away from home while supervising the building of the aqueduct bore a personal cost. His wife Lillie, suffering from cancer, could not attend the Cascade ceremony. S…”
- [ ] geology-and-water-resources-ov-report.pdf — KW #4 p100 · T3 institutional_bias/mild
  - “). The total quantity of recharge from runoff under average conditions of precipitation and evaporation is probably less than 1,000 acre-ft/yr (table 6). Owens River and …”
- [ ] owensvalleyhistory/ov_desert_news__page122.html.txt — KW #5 · T2 none/none
  - “al authorized bed capacity of 2840. Secretary McKay planned economic aid by organizing a non-profit corporation to conduct privately-financed economic surveys with an eye…”
- [ ] owensvalleyhistory/stories__mt_whitney_trail.pdf.pdf — KW #6 p1 · T2 none/none
  - “by pack trains, the army, and recreationalists for several decades following its completion. The trail was named after the founder, John B. Hockett, in 1863. It was being…”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #1 0.3159 · T2 none/none
  - “. Matlick] has in pasture 115 acres and has 38 milk cows (probably Durham cattle)...He finishes up about 50 head of beef creatures annually. This year he will have about …”
- [ ] owensvalleyhistory/stories__chronological_history_ov.pdf.pdf — IX #2 0.1697 · T2 none/none
  - “The Nevada and California Railroad (now Southern Pacific) extended the Owenyo line north from Mojave into the Owens Valley to serve the construction of the Los Angeles Aq…”
- [ ] owensvalleyhistory/stories__police_ready.pdf.pdf — IX #3 0.1394 · T2 none/none
  - “ standard railroad connection with the outside world. PURCHASE NECESSARY Unable to reach any sort of equitable agreement with valley interests concerning division and use…”
- [ ] owensvalleyhistory/stories__big_pine_fate.pdf.pdf — IX #4 0.0912 · T2 none/none
  - “1 BIG PINE’S FATE HOVERS OVER TOWN OF BISHOP, CALL WRITER LEARN’S Here is the fourth of a series of dramatic fact stories of the tragedy that has overtaken the Owens Rive…”
- [ ] owensvalleyhistory/stories__white_gold_disaster.pdf.pdf — IX #5 0.0522 · T2 none/none
  - “1 ‘WHITE GOLD’ CARRIES DISASTER TO PIONEERS OF OWENS RIVER VALLEY Here is the fifth of a series of dramatic fact stories of the tragedy that has overtaken the Owens River…”
- [ ] owensvalleyhistory/stories__phillips_padre_of_desert_1947.pdf.pdf — IX #6 0.0493 · T2 none/none
  - “ of his large congregation in Bishop, he was authorized to build a new church. The week after it was completed, Los Angeles launched its buying campaign of 1923-24 in Owe…”
- [ ] owensvalleyhistory/ov_aqueduct__page19.html.txt — IX #9 0.0124 · T2 none/none
  - “ to be bought, bings the city into ownership of what they term "98 percent of the water bearing lands in Mono Basin." Practically the same small ration of lands remain pr…”
- [ ] owensvalleyhistory/stories__Inyo County by Sunset Magazine_june 1912.pdf.pdf — IX #11 0.0058 · T2 none/none
  - “snow , which , melting , feeds the river and its tributaries the year round . Because of this the Inyo farmers ' crops never fail . Owens Valley , including also its subd…”
- [x] none

## 31. What legal battles did Owens Valley residents pursue against the City of Los Angeles over water rights?

- [x] owensvalleyhistory/ov_aqueduct__page19.html.txt — IX #2 0.9981 · KW #3 · T2 none/none
  - “- 1929 Owens River winding its way through Owens Valley Regulating gates on main canal in Owens Valley - 1912 Transformer float for Dredge No. 4l in Owens Valley - 190…”
- [x] owensvalleyhistory/ov_aqueduct__page20c.html.txt — IX #1 0.9994 · KW #7 · T2 none/none
  - “Los Angeles Aqueduct - Valley Rebellion Owens Valley's - Los Angeles Aqueduct If I am not on the JOB, You can find me at the AQUEDUCT was the rallying cry for t…”
- [x] water-land-history-oviwc.pdf — IX #6 0.9885 · KW #2 p3 · T1 primary_indigenous/none
  - “Valley Indian Water Commission (“Commission”) in 1991. The Fort Independence Reservation joined membership in the Commission in 1992. Since its inception, the C…”
- [x] owensvalleyhistory/stories__big_pine_fate.pdf.pdf — IX #3 0.9968 · T2 none/none
  - “Here, then, is the main theater of the Owens Valley water battle. SMALL FARMS Immediately adjacent to the town of Bishop lie 54,000 acres of irrigated lands. Every acre i…”
- [ ] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — KW #1 p4 · T2 none/none
  - “Owens Valley in the spring of 1905, giving residents the impression that he was purchasing water rights for the federal reclama­ tion project. Owens Valley farm…”
- [ ] owensvalleyhistory/stories__police_ready.pdf.pdf — IX #4 0.9958 · T2 none/none
  - “ that has been conducted against this city and its Department of Water and Power for more than three years. From the beginning this campaign has been characterized by fla…”
- [ ] owensvalleyhistory/stories__hydro electric developmens in southern ca.pdf.pdf — KW #4 p89 · T2 none/none
  - “ul Francisquito No. 1 went into operation; it was the first city-owned hydroelectric plant to deliver energy to Los Angeles. On January 21, 1913, the Los Angelés Times pu…”
- [ ] owensvalleyhistory/stories__never_the_same.pdf.pdf — IX #7 0.9884 · T2 none/none
  - “Things Will Never Quite be the Same The City of Los Angeles quickly and quietly began the process of acquiring water rights through permits, condemnations and outright la…”
- [ ] chronicling-america/stealing-owens-river-supply-july-30-1905.pdf — KW #5 · T2 institutional_bias/severe
  - “assert that they can pay for It out of the water revenue fund. MULHOLLAND OUTLINES PLAN Says It Is Opportunity Which Comes Once Ina MillionYeara Itis to Superintendent of…”
- [ ] owensvalleyhistory/jd_black_collection__page20e.html.txt — IX #9 0.9848 · T2 none/none
  - “J.D. Black Scrapbook Owens Valley's - Los Angeles Aqueduct All photographs on this pags are from the J. D. Black Collection digital archives located in the unless otherwi…”
- [ ] owensvalleyhistory/stories__walter_chalfant_story.pdf.pdf — KW #6 p1 · T2 none/none
  - “peaks of the High Sierra and the grotesque beauty of Death Valley and the desert. His life has been full of action, of editorial battles fought and won, of civic leadersh…”
- [ ] owensvalleyhistory/stories__owens_valley_facts_printed.pdf.pdf — IX #12 0.9783 · T2 none/none
  - “ seemed strong in favor of the people of Owens Valley.” “This publicity has hurt Los Angeles terribly. Los Angeles, with her billions of dollars of invested capital, cann…”
- [ ] none

## 32. How did the Dust Bowl of Owens Lake affect surrounding communities in terms of air quality and public health?

- [x] owensvalleyhistory/stories__keeping_dust_down.pdf.pdf — IX #1 0.9698 · KW #3 p2 · T2 none/none
  - “the ambient particles swirling over the basin were a major health hazard — and a violation of the federal Clean Air Act. Owens Lake is the largest single source of tiny p…”
- [ ] geology-and-water-resources-ov-report.pdf — KW #1 p89 · T3 institutional_bias/mild
  - “ty Socks" (table 5), which taps the lacustrine sediments of Owens Lake, is classified as C4-S4, an extremely poor-quality water for irrigation. In general, the ground wat…”
- [ ] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — KW #2 p20 · T2 none/none
  - “15 POINTS OF INTEREST IN THE OWENS RIVER VALLEY Owens Lake is a 100 square mile alkali lake that famously dried up after the city of Los Angeles diverted the region's wat…”
- [ ] owensvalleyhistory/stories__owens_lake_land_use_REDUCED.pdf.pdf — IX #3 0.1236 · KW #4 p2 · T2 none/none
  - “tilized in the analysis included the State Lands Commission Public Trust Doctrine,18 the Bishop Resource Management Plan,19 the California Desert Conservation Area Plan,2…”
- [ ] owensvalleyhistory/stories__soda_ash_industry.pdf.pdf — KW #5 p17 · T2 none/none
  - “in the West. The last plant to produce refined soda ash at Owens Lake was the PPG facility, which closed in 1968 (Table 1). Lake Minerals Cor­ poration, which is a joint …”
- [ ] owensvalleyhistory/stories__marshall cohen_OV Radio Observatory - Part 1.pdf.pdf — KW #6 p7 · T2 none/none
  - “ery Long Baseline Array. The DWP is the biggest employer in Owens Valley, but there still is contention between the valley's citizens and the city of Los Angeles. Particu…”
- [ ] owensvalleyhistory/owens_valley_owens_lake__page99.html.txt — IX #5 0.0067 · KW #10 · T2 none/none
  - “Owens Valley, Owens Lake,Owens River, Bartlett Owens Valley, Owens Lake & Bartlett, CA See on Home Page. Fotocards courtesy of the Rich McCutchan Archives unles…”
- [ ] owensvalleyhistory/stories__a_lake_no_more.pdf.pdf — IX #2 0.187 · T2 none/none
  - “1 A Lake No More Before diversions began, Owens Lake covered over 100 square miles of the Owens Valley floor. Steamships had once plied its water carrying silver bullion …”
- [ ] owensvalleyhistory/ghosts_of_past2__page9.html.txt — IX #6 0.0039 · T2 none/none
  - “ to fishing because of severe poaching, and giardia was introduced to the streams of the area. What a terrible price to pay for a road to nowhere. Sherman Stevens Sawmill…”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #7 0.003 · T2 none/none
  - “ Bishop Creek. A Los Angeles businessman, Fred Eaton, bought a sizable tract of land below Mono Lake in Long Valley with the intent to sell the land for a reservoir. Huge…”
- [ ] owensvalleyhistory/stories__death valley men_COMPRESSED.pdf.pdf — IX #9 0.0023 · T2 none/none
  - “ Lake. The chemical plants extract soda and allied salts from the thick saline solution which is Owens Lake. The lake is unbeautiful and the soda works, through which the…”
- [ ] owensvalleyhistory/stories__where_have_ranches_gone.pdf.pdf — IX #11 0.0002 · T2 none/none
  - “0. People were hungry, maybe poor people ate some of it. Even today the city of Los Angeles still is pumping water from underneath Owens Valley and getting away with it. …”
- [ ] none

## 33. What role did the Bureau of Reclamation play in Owens Valley water disputes?

- [x] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — IX #1 0.8179 · KW #2 p4 · T2 none/none
  - “one of the first areas picked to be surveyed for a possible reclamation project was the Owens Valley. It was not the only site. Frederick H. Newell, chief engineer of the…”
- [x] water-land-history-oviwc.pdf — IX #2 0.7546 · KW #10 p3 · T1 primary_indigenous/none
  - “ited States.” During that same year the Tribes, through the Owens Valley Indian Water Commission and Bureau of Indian Affairs (BIA), contracted with Natural Resources Con…”
- [x] california-geography-ch5-water.pdf — KW #1 p12 · T3 academic/none
  - “Obtaining Water Rights - 1902–1907 At the start of the 20th century, the United States Bureau of Reclamation, at the time known as the United States Reclamation Service,…”
- [x] owensvalleyhistory/stories__owens_valley_facts_printed.pdf.pdf — IX #5 0.4458 · KW #9 p2 · T2 none/none
  - “great calamity, when your community was being strangled for water, sufficient water was daily flowing through the irrigation canals of the Owens Valley ranchers to have d…”
- [ ] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — IX #9 0.1617 · KW #3 p4 · T2 none/none
  - “position of supervising engineer for California in the U.S. Reclamation Service. When Congress approved the creation of the Reclamation Service as an agency of the Depart…”
- [ ] owensvalleyhistory/stories__hydro electric developmens in southern ca.pdf.pdf — KW #4 p93 · T2 none/none
  - “71 Expansion became the keynote of the Bureau*a policies. Pasadena officials voted to accept the Bureau* s bid to supply electrical energy to that city at wholesale price…”
- [ ] story-of-inyo.pdf — KW #5 p352 · T3 settler_bias/moderate
  - “324 THE STORY OP INYO During the time that reclamation project in- vestigations had been under way in Owens Val- ley under Lippincott's supervision, he had been employed …”
- [ ] owensvalleyhistory/stories__valley_of_broken_hearts.pdf.pdf — IX #3 0.5862 · T2 none/none
  - “ but we knew something must be wrong. Finally we learned that the Reclamation plans had been abandoned and the whole water system had been turned over to Los Angeles. All…”
- [ ] owensvalleyhistory/stories__brown_meet_chalfant_of_inyo_1943.pdf.pdf — KW #6 p5 · T2 none/none
  - “Meet – Chalfant of Inyo 5 Before ever there was a reclamation act, enterprising homesteaders had located eight reservoir sites and had sought government permission to bui…”
- [ ] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #6 0.3384 · T2 none/none
  - “1 STRUGGLE FOR WATER IN OWENS VALLEY IS TOLD BY CALL STAFF WRITER Here is the second of a series of dramatic fact stories of the tragedy that has overtaken the Owens Rive…”
- [ ] owensvalleyhistory/stories__lippincott_biography.pdf.pdf — IX #10 0.1556 · T2 none/none
  - “Page 1 of 3 Biographical Information Joseph Barlow Lippincott Joseph Barlow Lippincott* was born in Scranton, Pa., on October 10, 1864, the son of Joshua Allen and Harrie…”
- [ ] owensvalleyhistory/ov_aqueduct__page20c.html.txt — IX #11 0.1427 · T2 none/none
  - “ have examined the situation that the city's purchases of valley lands have wrought a grave financial hardship on business man and property owners in the valley towns. Th…”
- [ ] none

## 34. Describe the relationship between the City of Los Angeles and Inyo County over water and land ownership.

- [x] owensvalleyhistory/stories__never_the_same.pdf.pdf — IX #1 0.9899 · KW #2 · T2 none/none
  - “Things Will Never Quite be the Same The City of Los Angeles quickly and quietly began the process of acquiring water rights through permits, condemnations and outright la…”
- [x] owensvalleyhistory/stories__life_goes_on.pdf.pdf — IX #2 0.9888 · KW #5 · T2 none/none
  - “But Life Goes On With very little land now available for purchase, the prospects for any future growth in Inyo County looked bleak. Scores of failing business owners now …”
- [x] owensvalleyhistory/ov_aqueduct__page19.html.txt — IX #3 0.9759 · KW #7 · T2 none/none
  - “l be a high speed one and will be the short route east from Los Angeles. It is the intention, I understand, of the company to connect the road with the narrow gauge, that…”
- [x] owensvalleyhistory/stories__police_ready.pdf.pdf — IX #4 0.9292 · KW #6 p5 · T2 none/none
  - “Police Ready to Rush North 5 to carry forward such water storage and conservation measures as would assure this 30,000-acre area a 100 percent water supply at all times. …”
- [ ] owensvalleyhistory/stories__owens_lake_land_use_REDUCED.pdf.pdf — KW #1 p8 · T2 none/none
  - “Land Ownership in the Owens Lake Area FIGURE 3.6.2-1 o 0 2 4 1 Miles 1:140,000 PropertyOwnership Bureau of Land Management City of Los Angeles Department of Wat…”
- [ ] owensvalleyhistory/stories__white_gold_disaster.pdf.pdf — KW #3 p1 · T2 none/none
  - “of the tragedy that has overtaken the Owens River Valley in Inyo County, where almost the entire population is facing an enforced migration due to the loss of its irrigat…”
- [ ] ov-native-water-story.pdf — KW #4 p2 · T1 primary_indigenous/none
  - “alfalfa. Because they had stolen the rich soils of our homeland, we moved to the sites, we began to make homes in the areas we once lived on and became day laborers for t…”
- [ ] payahuunadu-oviwc.pdf — IX #7 0.8765 · T1 primary_indigenous/none
  - “’s resources and carefully harvested its seed concentrations in order to sustain the land while living upon it. This was a longstanding, ecologically sustainable means of…”
- [ ] owensvalleyhistory/stories__the_gridiron_civil war threatened.pdf.pdf — IX #8 0.8453 · T2 none/none
  - “ seemed to mock us, we, too, would be thinking in terms of dynamite and guns.” Frederick Faulkner, in the Sacramento Union, says: “I experience a sense of failure at havi…”
- [ ] owensvalleyhistory/ov_aqueduct__page20c.html.txt — IX #10 0.8039 · T2 none/none
  - “ers on one side and the great city of Los Angeles on the Other. It is a drama that has been enacted on a smaller scale many times in California, with water as the cause o…”
- [ ] water-land-history-oviwc.pdf — IX #11 0.7765 · T1 primary_indigenous/none
  - “ to as the “Indian Problem”. The City of Los Angeles offered to exchange 1,511 acres of City-owned lands for 3,126 acres of federally reserved Indian lands. As described …”
- [ ] none

## 35. How did indigenous land use practices in Owens Valley differ from those of white settlers in the late 1800s?

- [x] ov-native-water-story.pdf — IX #1 0.9438 · KW #4 p1 · T1 primary_indigenous/none
  - “st rate with fine grasses and noted that large areas of the valley were being irrigated. Figure 2: Von Schmidt map. The Owens Valley Indian Water Commission. In 1859 Capt…”
- [x] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — IX #3 0.8745 · KW #2 p6 · T2 none/none
  - “1 POINTS OF INTEREST IN THE OWENS RIVER VALLEY A visit to Californiaʼs Owens River Valley serves as a case study for understanding the reach of the city and the reshaping…”
- [x] payahuunadu-oviwc.pdf — IX #4 0.8653 · KW #5 p4 · T1 primary_indigenous/none
  - “The delicate balance that we maintained in our use of water and land was interrupted when settlers came into the valley in the 19 th century. Settlers did not recognize t…”
- [x] water-land-history-oviwc.pdf — IX #6 0.7164 · KW #8 p1 · T1 primary_indigenous/none
  - “The Federal Reserved Indian Water Rights appurtenant to the lands traded in the 1939 Land Exchange remain unresolved. In addition to the Federal Reserved Indian Water Rig…”
- [ ] california-geography-ch5-water.pdf — KW #1 p11 · T3 academic/none
  - “d to raise cattle on the luxuriant grasses that grew in the Owens Valley. The ranchers came into conflict with the Paiutes over land and water use, and most of the Paiute…”
- [ ] fauna-flora-ov.pdf — IX #7 0.4841 · KW #6 p2 · T2 none/none
  - “face of change and others require intervention. The Owens Valley is prime example of a place where time appears to have stood still and yet the consequences of human acti…”
- [ ] geology-and-water-resources-ov-report.pdf — KW #3 p107 · T3 institutional_bias/mild
  - “ed canals and ditches and from water that is applied to the land. The water conveyed in the smaller canals and ditches is used primarily for sprinkler and flood irrigatio…”
- [ ] owensvalleyhistory/el_camino_sierra_tales__page111.html.txt — IX #5 0.82 · T2 none/none
  - “art uttered his famous final line, "That's what you think coppers" before being brought down by police sharpshooters. Lucille Ball and Desi Arnaz' character's fateful tri…”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #9 0.3775 · KW #9 p2 · T2 none/none
  - “k History Page 2 There were Paiute Indians living along the Owens River and Bishop Creek. They were a friendly people and few incidents of friction occurred between them …”
- [ ] owensvalleyhistory/stories__time_changes.pdf.pdf — IX #10 0.3332 · T2 none/none
  - “Times Change for Everyone It's estimated that as many as 2,000 Native Americans called Inyo and the Eastern Sierra home when white European settlers first arrived m the m…”
- [ ] none

## 36. What items did the Owens Valley Paiute primarily manufacture before 1910?

- [x] owensvalleyhistory/bishop_residents2__page48cc.html.txt — IX #2 0.4956 · KW #4 · T2 none/none
  - “Owens Valley Shoshone - Paiutes Owens Valley Paiute - Bishop, CA Owens Valley Shoshone - Paiutes Bishop - 5 Joe Bowers - Owens Valley Paiute (Courtesy J.D. Blac…”
- [x] owensvalleyhistory/stories__andrew_a_forbes_ovh_photographer.pdf.pdf — KW #1 p13 · T2 none/none
  - “PHOTOGRAPHS OF OWENS VALLEY PAIUTE 49 Fig. 11. Piutes (four unidentified women). The seated women wear necklaces made primarily of glass beads, the one on the left wearin…”
- [ ] ethnography-of-owens-valley-paiute.pdf — IX #3 0.2273 · KW #3 p43 · T1 academic/mild
  - “Steward: Ethnography of Owens Valley Paiute Theoretical aspects.-Two kinds of pottery were made in Owens val- ley: (1) large, round-bottom vessels from archaeological sit…”
- [ ] owensvalleyhistory/stories__owens_valley_rock_art.pdf.pdf — KW #2 p42 · T2 none/none
  - “nk. Small chippings were few, indicating that this site was primarily used for obtaining the raw material from which to manufacture tools.…”
- [ ] owensvalleyhistory/stories__chronological_history_ov.pdf.pdf — IX #1 0.6884 · T2 none/none
  - “The Nevada and California Railroad (now Southern Pacific) extended the Owenyo line north from Mojave into the Owens Valley to serve the construction of the Los Angeles Aq…”
- [ ] geology-and-water-resources-ov-report.pdf — KW #5 p74 · T3 institutional_bias/mild
  - “ns and through the volcanic rocks and moves south along the valley towards the narrows. Discharge from hydrogeologic unit 3 is primarily to wells, upward to hydrogeologic…”
- [ ] owensvalleyhistory/stories__armstrong_why_owens_lake_is_red_1981.pdf.pdf — KW #6 p1 · T2 none/none
  - “onds and lakes, were an important food in the diet of local Paiute Indians. The pupae, which look like grains of rice, occur in enormous numbers and can still be found ar…”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #5 0.1188 · T2 none/none
  - “ordo Freighting company, based in Mojave, California. His travels took him through Bishop in the beautiful Owens Valley. It captivated Al from the moment he first saw it.…”
- [ ] owensvalleyhistory/independence__page69.html.txt — IX #6 0.0639 · T2 none/none
  - “Pack Train heading up Kearsarge Pass Pack Train heading up Kearsarge Pass Snow covered Onion Valley Road Owens Valley - 1931 Snow covered Onion Valley Road Owens Valley -…”
- [ ] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — IX #7 0.0457 · T2 none/none
  - “ the benefits of irrigation. But irrigation demanded water already on the ground, not waiting for it to fall from the sky. Meanwhile, some 250 miles to the north, another…”
- [ ] owensvalleyhistory/owens_valley_owens_lake__page99.html.txt — IX #8 0.0412 · T2 none/none
  - “ never forget. I was 13 at the time. December 2025 Deb Drew-Goodman writes: My grandmother told me she remembers seeing the cloud rise above the Coso range south of Lone …”
- [ ] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #11 0.034 · T2 none/none
  - “1 STRUGGLE FOR WATER IN OWENS VALLEY IS TOLD BY CALL STAFF WRITER Here is the second of a series of dramatic fact stories of the tragedy that has overtaken the Owens Rive…”
- [ ] none

## 37. What was the role of the Los Angeles Times in shaping public opinion about the Owens Valley aqueduct project?

- [x] owensvalleyhistory/stories__aqueduct_history.pdf.pdf — IX #1 0.9557 · KW #5 p1 · T2 none/none
  - “1 L. A. AQUEDUCT HISTORY IS TOLD Here is the eighth of a series of dramatic fact stories of the tragedy that has overtaken the Owens River Valley in Inyo County, where…”
- [x] owensvalleyhistory/ov_aqueduct__page18.html.txt — IX #4 0.9251 · KW #2 · T2 none/none
  - “Lippincott, Fred A. Eaton, and William Mulholland (1906 Los Angeles Times Photo) Los Angeles Board of Water Commissioners at the time of the building of the Los Angeles a…”
- [x] owensvalleyhistory/jd_black_collection__page20e.html.txt — IX #3 0.9293 · KW #4 · T2 none/none
  - “J.D. Black Scrapbook Owens Valley's - Los Angeles Aqueduct All photographs on this pags are from the J. D. Black Collection digital archives located in the unless otherwi…”
- [x] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — IX #7 0.8466 · KW #3 p4 · T2 none/none
  - “holland’s assistant chief engineer on the construc­ tion project. Prior to taking on that task, however, Lippincott held the position of supervising engineer for Californ…”
- [ ] owensvalleyhistory/ov_aqueduct__page20c.html.txt — IX #2 0.9346 · T2 none/none
  - “Los Angeles Aqueduct - Valley Rebellion Owens Valley's - Los Angeles Aqueduct If I am not on the JOB, You can find me at the AQUEDUCT was the rallying cry for the people …”
- [ ] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — KW #1 p6 · T2 none/none
  - “support for an Owens River Aqueduct. Rumors flew around Owens Valley in the spring of 1905 as to what was going on, but public announcement did not appear until July 29. …”
- [ ] owensvalleyhistory/stories__alan_seeks_water_facts.pdf.pdf — IX #11 0.7567 · KW #6 p1 · T2 none/none
  - “esolution to Ask Mayor and Service Board To Reveal Plans in Aqueduct Row Los Angeles Daily Times 11-20-1924 Councilman Allan announced yesterday that in order that the Ci…”
- [ ] owensvalleyhistory/stories__owens_valley_facts_printed.pdf.pdf — IX #5 0.884 · T2 none/none
  - “1 OWENS VALLEY ‘FACTS’ PRINTED “Greed of City” Declared to be Ruining ranchers Bishop Paper Points Shortage Here Great Calamity Effort to Wreck Irrigation Bonds Value Cha…”
- [ ] owensvalleyhistory/ov_aqueduct__page19.html.txt — IX #9 0.7843 · T2 none/none
  - “Los Angeles Aqueduct - Owens Valley Owens Valley's - Los Angeles Aqueduct Unless otherwise note, All L.A. aqueduct photographs on these pages are from the unless otherwis…”
- [ ] none

## 38. Describe the irrigation systems that Owens Valley farmers built before Los Angeles acquired their water rights.

- [x] water-land-history-oviwc.pdf — IX #2 0.9914 · KW #5 p1 · T1 primary_indigenous/none
  - “zed the Secretary of Interior to exchange certain lands and water rights with the City of Los Angeles provided that: City lands being exchanged were of more value than th…”
- [x] owensvalleyhistory/stories__big_pine_fate.pdf.pdf — IX #1 0.995 · KW #7 p2 · T2 none/none
  - “pro rata basis among the farmers. A miner’s inch of water is deemed necessary in the valley for the irrigation of one acre of land. The normal flow of the Owens River whe…”
- [x] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #8 0.9652 · KW #6 p4 · T2 none/none
  - “Valley of Broken Hearts – Part 2 4 They will even remind you, if the thought had not occurred to you, that for every acre brought under cultivation about the to…”
- [x] owensvalleyhistory/el_camino_sierra_tales__page111.html.txt — IX #3 0.9882 · T2 none/none
  - “ Valley into an agricultural super farm. The committee saw the abundant water in the streams from the Sierra Nevada (this was pre L.A. diversions) and concluded the use o…”
- [ ] california-geography-ch5-water.pdf — KW #1 p13 · T3 academic/none
  - “dressing the Crowd at the Opening of the Aqueduct. Image by Los Angeles Department of Water and Power is in the public domain. After the aqueduct was completed in 1913, t…”
- [ ] owensvalleyhistory/jd_black_collection__page20e.html.txt — IX #4 0.9807 · T2 none/none
  - “J.D. Black Scrapbook Owens Valley's - Los Angeles Aqueduct All photographs on this pags are from the J. D. Black Collection digital archives located in the unless otherwi…”
- [ ] owensvalleyhistory/stories__Tragedy_stalks_valley_of_broken_hearts.pdf.pdf — KW #2 p2 · T2 none/none
  - “Valley of Broken Hearts – Part 3 2 Then came the sale of the lands under the McNally ditch to the north of them. Under the pressure of its need for more water,…”
- [ ] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — KW #3 p6 · T2 none/none
  - “r 1904 Mulholland, Eaton, and Lippincott met with Newell in Los Angeles. Mulholland promised Newell that any project undertaken by Los Angeles would be wholly municipal i…”
- [ ] owensvalleyhistory/stories__never_the_same.pdf.pdf — IX #5 0.9729 · T2 none/none
  - “Things Will Never Quite be the Same The City of Los Angeles quickly and quietly began the process of acquiring water rights through permits, condemnations and outright la…”
- [ ] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — KW #4 p4 · T2 none/none
  - “Owens Valley in the spring of 1905, giving residents the impression that he was purchasing water rights for the federal reclama­ tion project. Owens Valley farm…”
- [ ] owensvalleyhistory/stories__chronological_history_ov.pdf.pdf — IX #6 0.9712 · T2 none/none
  - “The Nevada and California Railroad (now Southern Pacific) extended the Owenyo line north from Mojave into the Owens Valley to serve the construction of the Los Angeles Aq…”
- [ ] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — IX #9 0.9574 · T2 none/none
  - “POINTS OF INTEREST IN THE OWENS RIVER VALLEY POINTS OF INTEREST IN THE OWENS RIVER VALLEY A Center for Land Use Interpretation publication The contents of this book are p…”
- [ ] none

## 39. What happened to the town of Keeler, California after Owens Lake dried up?

- [x] owensvalleyhistory/carson_n_colorado__page51h.html.txt — IX #4 0.9822 · KW #1 · T2 none/none
  - “to the SP shops in Bakersfield, California. However, the daily maintenance all took place in the rain, snow or sunshine outside at this spot in Keeler. The line lasted in…”
- [x] owensvalleyhistory/keeler__page71.html.txt — IX #1 0.9968 · KW #5 · T2 none/none
  - “Inyo Range as a backdrop, before water disappeared from the lake. [photo: Eastern California Museum collection] Locally built Keeler pool, August 9, 1929. People gathered…”
- [x] owensvalleyhistory/stories__millspaugh_bessie_brady_1971.pdf.pdf — IX #3 0.9898 · KW #4 p2 · T2 none/none
  - “s will take you to the marshy and salt-crusted shore of the lake. It was here the steamer was loaded with charcoal and lumber for her trip across the lake to the smelters…”
- [x] owensvalleyhistory/cerro_gordo1__page44.html.txt — IX #6 0.9724 · KW #7 · T2 none/none
  - “Cerro Gordo 2 Keeler terminus on the . "Fat Hill" See on Home Page Bob Likes Pictures and text excerpts are all from " From this Mountain - Cerro Gordo " by Robert C. Lik…”
- [ ] owensvalleyhistory/stories__southern_inyo.pdf.pdf — IX #2 0.9912 · T2 none/none
  - “ through wheel-swallowing sand. A pair of lake steamers was built: the Bessie Brady and the Mollie Stevens. The loaves of silver-lead bullion piled up at the bottom of Ye…”
- [ ] owensvalleyhistory/keeler__page71a.html.txt — IX #9 0.9598 · KW #6 · T2 none/none
  - “Old NSP Co., Keeler, CA - 1925 Bishop, California - 1921 David Olds Farm (C.L. Olds top left- David and Nettie Olds on far right) Bishop, CA - 1885 David Olds farm (Netti…”
- [ ] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — KW #2 p23 · T2 none/none
  - “POINTS OF INTEREST IN THE OWENS RIVER VALLEY 18 Keeler is the only existing settlement on the east side of Owens Lake. Through the 19th and early 20th century, the town h…”
- [ ] owensvalleyhistory/owens_valley_owens_lake__page99.html.txt — KW #3 · T2 none/none
  - “from Los Angeles to the Owens Valley. (Photo courtesy of the ) 10/23 Owens Lake (Photo courtesy of the Online Archive of California ) by Marius R. Campbell (Article court…”
- [ ] owensvalleyhistory/bessie_brady__page23.html.txt — IX #5 0.9795 · T2 none/none
  - “ 395 at the sign just north of Cartago and drive a short distance to the east. A short walk beyond the kilns will take you to the marshy and salt-crusted shore of the lak…”
- [ ] owensvalleyhistory/keeler__page71d.html.txt — IX #7 0.9711 · T2 none/none
  - “Keeler Keeler, California All photo cards courtesy of Rich McCutchan unless otherwise noted. See on Home Page. 05/21 Aerial photos courtesy Aerial view of Keeler - Octobe…”
- [ ] none

## 40. How did the Second Los Angeles Aqueduct differ from the first in terms of construction and impact?

- [x] ov-native-water-story.pdf — IX #1 0.9917 · KW #1 p2 · T1 primary_indigenous/none
  - “ship and created our new norm of existing in our homelands. Los Angeles’ Water Schemes Then this situation changed once again. Why did this change? Because Los Angeles an…”
- [x] owensvalleyhistory/ov_aqueduct__page20b.html.txt — IX #4 0.5857 · KW #2 · T2 none/none
  - “Hauling pipe sections into place Photo from the 1916 book "Construction of the Los Angeles Aqueduct Final Report " by the Board of Public Service Commissioners of the Cit…”
- [x] owensvalleyhistory/ov_aqueduct__page18.html.txt — IX #5 0.5388 · KW #8 · T2 none/none
  - “, and the adjacent Colorado River states. "When Rome falls (Los Angeles and its unquenchable thirst for water) there will be such a shout of freedom that the world will n…”
- [ ] owensvalleyhistory/ov_aqueduct__page20a.html.txt — KW #3 · T2 none/none
  - “Los Angeles Aqueduct - Rose Valley Owens Valley's - Los Angeles Aqueduct Unless otherwise note, All L.A. aqueduct photographs on these pages are from the unless…”
- [ ] owensvalleyhistory/stories__aqueduct_history.pdf.pdf — IX #2 0.694 · T2 none/none
  - “1 L. A. AQUEDUCT HISTORY IS TOLD Here is the eighth of a series of dramatic fact stories of the tragedy that has overtaken the Owens River Valley in Inyo County, where al…”
- [ ] owensvalleyhistory/ov_aqueduct__page19.html.txt — KW #4 · T2 none/none
  - “ve, all of which will produce anything that can be grown in Los Angeles county, including oranges. It is to be hoped that very soon the railroad, as above proposed, will …”
- [ ] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — IX #3 0.6718 · T2 none/none
  - “ certainly commendable that it was completed under budget. Construction began in September 1907. Los Angeles voters overwhelmingly approved the bond issue to finance the …”
- [ ] geology-and-water-resources-ov-report.pdf — KW #5 p28 · T3 institutional_bias/mild
  - “important water-bearing formations. As demand for water in Los Angeles increased, the Los Angeles Department of Water and Power collected large quantities of data on stre…”
- [ ] owensvalleyhistory/ov_aqueduct__page20.html.txt — KW #6 · T2 none/none
  - “Los Angeles Aqueduct - Olancha Owens Valley's - Los Angeles Aqueduct Unless otherwise note, All L.A. aqueduct photographs on these pages are from the unless oth…”
- [ ] owensvalleyhistory/stories__Los_Angeles_Department_of_Water_and_Power_Operations_in_the_Mono_Basin.pdf.pdf — IX #6 0.2963 · KW #9 p8 · T2 none/none
  - “EXPORT OF 100,000 ACRE-FEET OF WATER FROM THE MONO BASIN TO Los ANGELES GENERATES ENERGY ALONG THE AQUEDUCT SYSTEM EQUIVALENT TO APPROXIMATELY 500,000 BARRELS OF FUEL OIL…”
- [ ] owensvalleyhistory/ov_aqueduct__mulholland1.html.txt — IX #8 0.1595 · T2 none/none
  - “ something about which my whole scheme of life was woven, I loved it so much." Proof of his devotion is indelibly written in his lifetime of service to the water needs of…”
- [ ] chronicling-america/indorse-owens-project-dec-25-1906.pdf — IX #10 0.1061 · T2 institutional_bias/severe
  - “,000,tH)0. ,iPress, Place Huge Steel Contracts "We therefore have as the total pow- er that may be developed under the 40 per cent load factor for the two canyon sites a …”
- [ ] none

## 41. Describe the role of the Owens Valley in supplying water during Los Angeles's early population boom.

- [x] water-land-history-oviwc.pdf — IX #1 0.9957 · KW #5 p1 · T1 primary_indigenous/none
  - “ain public lands from settlement …for the protection of the watershed supplying water to the city of Los Angeles and other cities and towns in the State of California, an…”
- [x] owensvalleyhistory/jd_black_collection__page20e.html.txt — IX #2 0.9917 · KW #9 · T2 none/none
  - “J.D. Black Scrapbook Owens Valley's - Los Angeles Aqueduct All photographs on this pags are from the J. D. Black Collection digital archives located in the unless otherwi…”
- [x] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — IX #10 0.9652 · KW #3 p4 · T2 none/none
  - “of the Los Angeles River was under a franchise granted to a private firm, the Los Angeles City Water Company. Mulholland went to work for the water company and rose th…”
- [x] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — IX #3 0.9894 · T2 none/none
  - “POINTS OF INTEREST IN THE OWENS RIVER VALLEY POINTS OF INTEREST IN THE OWENS RIVER VALLEY A Center for Land Use Interpretation publication The contents of this book are p…”
- [ ] geology-and-water-resources-ov-report.pdf — IX #8 0.97 · KW #7 p25 · T3 institutional_bias/mild
  - “canic Tableland (fig. 5). Of the 307,000 acres owned by the Los Angeles Department of Water and Power in Owens Valley and Mono Basin drainage basins, most of the land (24…”
- [ ] fauna-flora-ov.pdf — KW #1 p2 · T2 none/none
  - “face of change and others require intervention. The Owens Valley is prime example of a place where time appears to have stood still and yet the consequences of human acti…”
- [ ] payahuunadu-oviwc.pdf — IX #4 0.9884 · T1 primary_indigenous/none
  - “’s resources and carefully harvested its seed concentrations in order to sustain the land while living upon it. This was a longstanding, ecologically sustainable means of…”
- [ ] california-geography-ch5-water.pdf — KW #2 p11 · T3 academic/none
  - “the tributaries of the Owens River. Repurposing the canals and irrigation channels that the Paiute had originally created, as well as the addition by ditch companies, did…”
- [ ] owensvalleyhistory/ov_aqueduct__page20c.html.txt — IX #5 0.984 · T2 none/none
  - “ers on one side and the great city of Los Angeles on the Other. It is a drama that has been enacted on a smaller scale many times in California, with water as the cause o…”
- [ ] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — KW #4 p6 · T2 none/none
  - “the moment, he would consider running for mayor of Los Angeles. Mulholland rejected the idea. He said that he would rather give birth to a porcupine backwards than be may…”
- [ ] owensvalleyhistory/stories__aqueduct_history.pdf.pdf — IX #6 0.9768 · T2 none/none
  - “1 L. A. AQUEDUCT HISTORY IS TOLD Here is the eighth of a series of dramatic fact stories of the tragedy that has overtaken the Owens River Valley in Inyo County, where al…”
- [ ] owensvalleyhistory/stories__chronological_history_ov.pdf.pdf — IX #7 0.9732 · T2 none/none
  - “The Nevada and California Railroad (now Southern Pacific) extended the Owenyo line north from Mojave into the Owens Valley to serve the construction of the Los Angeles Aq…”
- [ ] owensvalleyhistory/manzanar_town__page56.html.txt — KW #6 · T2 none/none
  - “The main automobile road through the Owens Valley was unpaved at this time; much later it was paved from Mojave to Nevada and made an official State Highway (US 395), one…”
- [ ] none

## 42. What trade relationships existed between Owens Valley Paiute communities and neighboring tribes?

- [x] ethnography-of-owens-valley-paiute.pdf — IX #1 0.9937 · KW #3 p23 · T1 academic/mild
  - “Steward: Ethnography of Owens Valley Paiute yielded evidence in the form of pottery of a Pueblo culture, which pre- sumably included horticulture, as far west as Wellingt…”
- [x] payahuunadu-oviwc.pdf — IX #3 0.9861 · KW #4 p3 · T1 primary_indigenous/none
  - “Our Ecology Prior to Western Contact The Nüümü (Owens Valley Paiute) are a people born of water. Our oral histories, passed down from generation to generation, tell of th…”
- [x] water-land-history-oviwc.pdf — IX #4 0.897 · KW #2 p3 · T1 primary_indigenous/none
  - “1997 Principles of Agreement was not ratified by all of the Tribes because it lacked access to “wet” water, infrastructure funding, land acquisition, and the usual benefi…”
- [x] owensvalleyhistory/stories__owens_valley_rock_art.pdf.pdf — IX #11 0.3271 · KW #6 p9 · T2 none/none
  - “ral months. Before taking up a sedentary life, however, the tribes or groups pushed southward after the migrations in the fall had ended. Little Lake is over a hundred mi…”
- [ ] ov-native-water-story.pdf — IX #12 0.2325 · KW #1 p2 · T1 primary_indigenous/none
  - “created division amongst the Tribes in the Owens Valley and Eastern Sierra, the Owens Valley Indian Water Commission continues to work with environmental staff from all t…”
- [ ] owensvalleyhistory/stories__andrew_a_forbes_ovh_photographer.pdf.pdf — KW #5 p4 · T2 none/none
  - “o HoUister and the San Joaquin VaUey. His subjects included communities and landscapes. Death Vahey, the New Idria mercury mine, and fur trappers, among others. About 190…”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #8 0.4331 · T2 none/none
  - “ordo Freighting company, based in Mojave, California. His travels took him through Bishop in the beautiful Owens Valley. It captivated Al from the moment he first saw it.…”
- [ ] owensvalleyhistory/bishop_residents2__page48cc.html.txt — IX #9 0.4218 · T2 none/none
  - “Owens Valley Shoshone - Paiutes Owens Valley Paiute - Bishop, CA Owens Valley Shoshone - Paiutes Bishop - 5 Joe Bowers - Owens Valley Paiute (Courtesy J.D. Black Collecti…”
- [ ] owensvalleyhistory/independence__page69.html.txt — IX #13 0.1325 · T2 none/none
  - “Pack Train heading up Kearsarge Pass Pack Train heading up Kearsarge Pass Snow covered Onion Valley Road Owens Valley - 1931 Snow covered Onion Valley Road Owens Valley -…”
- [ ] none

## 43. How did the arrival of the railroad change economic and social life in Owens Valley?

- [x] owensvalleyhistory/stories__narrow_gauge_wilderness.pdf.pdf — IX #1 0.985 · KW #1 p3 · T2 none/none
  - “the Governor of Nevada in 1932. them all. Consequently the arrival of the narrow gauge was hardly mentioned as it wended its way down the eastern portion of the valley fl…”
- [x] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — IX #2 0.9776 · KW #5 p2 · T2 none/none
  - “rowth and development. American explorers first visited the Owens Valley in the 1830s; John C. Fremont named the valley in 1845 after one of his expedition's members. Beg…”
- [x] owensvalleyhistory/stories__chronological_history_ov.pdf.pdf — IX #3 0.9765 · T2 none/none
  - “ was in Robber's Roost, robbed stages and freight wagons along the eastern Sierra, especially near Coyote Wells (Freeman Junction) until he was captured later that year. …”
- [ ] owensvalleyhistory/stories__desert_padre_tales.pdf.pdf — KW #2 p1 · T2 none/none
  - “the east. Starting in the 1870s, early settlers trapped the Owens River to irrigate fields and orchards in the remote valley and created, for a short time, one of the mos…”
- [ ] owensvalleyhistory/stories__paradise_found.pdf.pdf — IX #4 0.9206 · T2 none/none
  - “Paradise Found The lack of reliable transportation to outside markets hindered the development of more large-scale, intense agriculture. The inability to ship agricultura…”
- [ ] owensvalleyhistory/stories__time_changes.pdf.pdf — KW #3 · T2 none/none
  - “Times Change for Everyone It's estimated that as many as 2,000 Native Americans called Inyo and the Eastern Sierra home when white European settlers first arrived m t…”
- [ ] owensvalleyhistory/carson_n_colorado__page51b.html.txt — KW #4 · T2 none/none
  - “of the majestic Grand Central Terminal in NYC. This career change gave me an appreciation for railroading that was hands on and I could only imagine what it was like in t…”
- [ ] owensvalleyhistory/manzanar_town__page56.html.txt — IX #5 0.8828 · T2 none/none
  - “ens Valley is on the route of the most attractive of all transcontinental automobile highways, the 'MIDLAND TRAIL.' The best natural route across Nevada comes into this V…”
- [ ] california-geography-ch12-great-basin.pdf — KW #6 p18 · T3 academic/none
  - “was moved by flume to the valley, where it was burned in adobe kilns to make charcoal, which was then transported by steamships across Owens Lake to the smelters at Swans…”
- [ ] owensvalleyhistory/stories__slim_princess.pdf.pdf — IX #7 0.7832 · T2 none/none
  - “ but it was common knowledge that they, together with Nicholas Luning, controlled all but a few shares of the stock. N Slim Princess Page 2 of 5 The C&C was a financial s…”
- [ ] owensvalleyhistory/stories__Inyo County by Sunset Magazine_june 1912.pdf.pdf — IX #9 0.7107 · T2 none/none
  - “snow , which , melting , feeds the river and its tributaries the year round . Because of this the Inyo farmers ' crops never fail . Owens Valley , including also its subd…”
- [ ] owensvalleyhistory/el_camino_sierra_tales__page111.html.txt — IX #11 0.5205 · T2 none/none
  - “ Valley into an agricultural super farm. The committee saw the abundant water in the streams from the Sierra Nevada (this was pre L.A. diversions) and concluded the use o…”
- [ ] none

## 44. Describe the seasonal migration patterns of Owens Valley Paiute families before white settlement.

- [x] owensvalleyhistory/stories__owens_valley_rock_art.pdf.pdf — IX #1 0.6826 · KW #8 p3 · T2 none/none
  - “the Great Basin pecked petroglyphs are associated with game migration trails and were fashioned at spots where the animals were hunted. J. Steward has suggested (1963:975…”
- [x] owensvalleyhistory/stories__northern paiutes of california and nevada.pdf.pdf — IX #3 0.3438 · KW #3 p43 · T2 none/none
  - “try to drive them off. This happened when the Whites first began to move into Paiute country and there was perhaps more fighting then than there had been for a long time …”
- [ ] owensvalleyhistory/stories__Horse Meadows and Bohler Canyon Arborglyphs.pdf.pdf — KW #1 p2 · T2 none/none
  - “out the high quality protein of mutton. Many of the pioneer families, the Filosenas, Sylvesters, Mathieus, Conways and DeChambeau’s, who accompanied this boom were ranche…”
- [ ] owensvalleyhistory/stories__jordan_hot_springs_resort_n_john_jordan_trail.pdf.pdf — KW #2 p12 · T2 none/none
  - “use strategies. And also to inquire what effect prehistoric settlement patterns had on land use choices made by Euroamericans; after all, it was Native Americans who led …”
- [ ] story-of-inyo.pdf — KW #4 p72 · T3 settler_bias/moderate
  - “e next expedition this way. It was the westernmost frontier settlement and the starting point of the sunset trails. In 1832 Walker left there as a lieutenant of Capt. Bon…”
- [ ] water-land-history-oviwc.pdf — IX #9 0.1166 · KW #5 p3 · T1 primary_indigenous/none
  - “ng, land acquisition, and the usual benefits found in water settlements. The agreement was essentially a “paper” water right and would put new restrictions on the existin…”
- [ ] owensvalleyhistory/stories__narrow_gauge_nowhere.pdf.pdf — KW #6 p2 · T2 none/none
  - “and Inyo. The settlement was established as the junction point between the standard gauge "Jawbone Branch," from Mojave and the narrow gauge in 1910. Most of the town's 7…”
- [ ] ethnography-of-owens-valley-paiute.pdf — IX #5 0.2311 · KW #10 p100 · T1 academic/mild
  - “Steward: Ethnography of Owens Valley Paiute APPENDIX: 1. PLACE NAMES AND KEY TO MAPS MAP 1 1. Tubogi, little caves. 2. Summer camp of Mono Lake Paiute in Little Yosemite.…”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #2 0.3788 · T2 none/none
  - “ordo Freighting company, based in Mojave, California. His travels took him through Bishop in the beautiful Owens Valley. It captivated Al from the moment he first saw it.…”
- [ ] owensvalleyhistory/stories__historic legends_COMPRESSED.pdf.pdf — IX #8 0.1172 · KW #9 p21 · T2 none/none
  - “ependence was continually garrisoned. With the army back in Owens Valley, most of the remaining Paiutes resumed their peaceful ways. A handful, however, never were able t…”
- [ ] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #4 0.2465 · T2 none/none
  - “1 STRUGGLE FOR WATER IN OWENS VALLEY IS TOLD BY CALL STAFF WRITER Here is the second of a series of dramatic fact stories of the tragedy that has overtaken the Owens Rive…”
- [ ] owensvalleyhistory/bishop_residents2__page48cc.html.txt — IX #6 0.1446 · T2 none/none
  - “Owens Valley Shoshone - Paiutes Owens Valley Paiute - Bishop, CA Owens Valley Shoshone - Paiutes Bishop - 5 Joe Bowers - Owens Valley Paiute (Courtesy J.D. Black Collecti…”
- [ ] payahuunadu-oviwc.pdf — IX #7 0.1438 · T1 primary_indigenous/none
  - “’s resources and carefully harvested its seed concentrations in order to sustain the land while living upon it. This was a longstanding, ecologically sustainable means of…”
- [ ] none

## 45. What was the significance of pine nuts in Owens Valley Paiute culture and subsistence?

- [x] payahuunadu-oviwc.pdf — IX #1 0.7737 · KW #4 p3 · T1 primary_indigenous/none
  - “ative grasses, grew taboose and nahativa, collected acorns, pine nuts, tubers, larva. The small pupfish that swam in the waters of Payahuunadü were collected, dried in th…”
- [x] owensvalleyhistory/stories__northern paiutes of california and nevada.pdf.pdf — IX #3 0.3942 · KW #3 p62 · T2 none/none
  - “so the accounts say, and killed several . They fought near Owens Lake too, getting to gether and building a fort, though they had never done such a thing before . However…”
- [x] owensvalleyhistory/stories__andrew_a_forbes_ovh_photographer.pdf.pdf — KW #1 p22 · T2 none/none
  - “IFORNIA ANTHROPOLOGY Fig. 20. The Winnower. A woman winnows pinenuts (pinon, Pinus monophylla) with an open twined win- nowing tray. Two other trays are on the ground bef…”
- [ ] ethnography-of-owens-valley-paiute.pdf — IX #6 0.0986 · KW #2 p10 · T1 academic/mild
  - “hn. [Vol. 33 guage, somewhat in mythology,4 and slightly in culture from the Paiute. The Shoshoni-Paiute dividing line ran from the Pilot mountains, Ne- vada, south throu…”
- [ ] owensvalleyhistory/stories__steven melvin_eichbaum_toll_road_history.pdf.pdf — KW #5 p36 · T2 none/none
  - “m Toll Road Historic Context June 2018 5. NATIONAL REGISTER SIGNIFICANCE Section 106 of the National Historic Preservation Act defines a historic property as a historic d…”
- [ ] california-geography-ch12-great-basin.pdf — KW #6 p17 · T3 academic/none
  - “a, and Whitney Portal Arch. In addition to their geological significance, the Alabama Hills are also culturally important. The hills have been used as a filming location …”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #2 0.4665 · T2 none/none
  - “ordo Freighting company, based in Mojave, California. His travels took him through Bishop in the beautiful Owens Valley. It captivated Al from the moment he first saw it.…”
- [ ] owens-valley-paiute-autobiographies.pdf — IX #5 0.1232 · KW #8 p6 · T1 academic/mild
  - “rch Mountain (Pau'okud- auwa) and heard a voice speaking in Paiute. Wondering about whence it came he went toward it and heard it say, "Nothing will happen to me. I will …”
- [ ] owensvalleyhistory/stories__Life in Southern California_The Gentleman's Magazine_january to june 1894.pdf.pdf — IX #12 0.0045 · T2 none/none
  - “ chains from the Sierras to the Rockies. This is the home of the Puite and the Shoshonee, of the “ side-winder ” rattlesnake, and of the horned toad. The hills are rich i…”
- [ ] owensvalleyhistory/stories__desert indians way of life_COMPRESSED.pdf.pdf — IX #13 0.0041 · T2 none/none
  - “THE DESERT INDIANS WAY OF LIFE For many years after William Lyle Hunter went with mules from Cerro Gordo to establish the Hunter Ranch, Indians from many parts of the des…”
- [ ] ov-native-water-story.pdf — IX #14 0.0039 · T1 primary_indigenous/none
  - “Payahǖǖnadǖ Water Story – Wading Through the Past Teri Red Owl This is our water story of Payahǖǖnadǖ, our homelands. We interpret the name as being the place where water…”
- [ ] none

## 46. How did Owens Valley ranchers and farmers organize politically to resist Los Angeles water acquisition?

- [x] owensvalleyhistory/ov_aqueduct__page20c.html.txt — IX #1 0.9984 · KW #2 · T2 none/none
  - “Los Angeles Aqueduct - Valley Rebellion Owens Valley's - Los Angeles Aqueduct If I am not on the JOB, You can find me at the AQUEDUCT was the rallying cry for t…”
- [x] owensvalleyhistory/stories__big_pine_fate.pdf.pdf — IX #3 0.9942 · KW #7 p2 · T2 none/none
  - “pro rata basis among the farmers. A miner’s inch of water is deemed necessary in the valley for the irrigation of one acre of land. The normal flow of the Owens River whe…”
- [x] owensvalleyhistory/ov_aqueduct__page19.html.txt — IX #7 0.9551 · KW #4 · T2 none/none
  - “ve, all of which will produce anything that can be grown in Los Angeles county, including oranges. It is to be hoped that very soon the railroad, as above proposed, will …”
- [x] owensvalleyhistory/stories__owens_valley_facts_printed.pdf.pdf — IX #13 0.8513 · KW #5 p2 · T2 none/none
  - “Owens Valley ‘Facts’ Printed 2 a doubt of the ability of irrigation districts to resist the encroachments of the great cities that need water fro domestic use.”…”
- [ ] owensvalleyhistory/jd_black_collection__page20e.html.txt — IX #4 0.9875 · T2 none/none
  - “J.D. Black Scrapbook Owens Valley's - Los Angeles Aqueduct All photographs on this pags are from the J. D. Black Collection digital archives located in the unless otherwi…”
- [ ] california-geography-ch5-water.pdf — KW #1 p13 · T3 academic/none
  - “dressing the Crowd at the Opening of the Aqueduct. Image by Los Angeles Department of Water and Power is in the public domain. After the aqueduct was completed in 1913, t…”
- [ ] owensvalleyhistory/stories__police_ready.pdf.pdf — IX #6 0.9605 · T2 none/none
  - “ that has been conducted against this city and its Department of Water and Power for more than three years. From the beginning this campaign has been characterized by fla…”
- [ ] owensvalleyhistory/stories__aqueduct_cascade.pdf.pdf — KW #3 p4 · T2 none/none
  - “Owens Valley in the spring of 1905, giving residents the impression that he was purchasing water rights for the federal reclama­ tion project. Owens Valley farm…”
- [ ] owensvalleyhistory/stories__never_the_same.pdf.pdf — IX #8 0.9112 · T2 none/none
  - “Things Will Never Quite be the Same The City of Los Angeles quickly and quietly began the process of acquiring water rights through permits, condemnations and outright la…”
- [ ] owensvalleyhistory/stories__time_changes.pdf.pdf — KW #6 · T2 none/none
  - “next several decades, so they did for the Native Americans. Water rights retained by the local Paiute-Shoshone were as aggressively sought after by the City of Los Angele…”
- [ ] owensvalleyhistory/stories__the_gridiron_civil war threatened.pdf.pdf — IX #9 0.8961 · T2 none/none
  - “ seemed to mock us, we, too, would be thinking in terms of dynamite and guns.” Frederick Faulkner, in the Sacramento Union, says: “I experience a sense of failure at havi…”
- [ ] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #10 0.8561 · T2 none/none
  - “ miles of desert. To the relinquishment of water for Los Angeles domestic use the people of Owens Valley have long since been reconciled. But to the use of this water for…”
- [ ] none

## 47. Describe the living conditions at the Fort Tejon reservation during the Paiute forced relocation.

- [x] payahuunadu-oviwc.pdf — IX #2 0.0177 · KW #1 p4 · T1 primary_indigenous/none
  - “mping. Next, they turned to the lands held in trust for the Paiute by the federal government. Between 1920 and 1930, as agricultural activities decreased due to land sale…”
- [ ] story-of-inyo.pdf — KW #2 p119 · T3 settler_bias/moderate
  - “in 1851. By 1853, he was virtually in charge of the Indian reservation at Fort Tejon. That year he and General Beale, later prominent in Kern County affairs, formed a par…”
- [ ] ov-native-water-story.pdf — IX #4 0.0038 · KW #3 p1 · T1 primary_indigenous/none
  - “ners and settlers there, I deem that locality for an Indian reservation entirely impractical.” Yet over 900 of my people were eventually forcibly marched by the United St…”
- [ ] owensvalleyhistory/stories__northern paiutes of california and nevada.pdf.pdf — IX #3 0.0122 · KW #4 p78 · T2 none/none
  - “24 . 33 25 . Paiute woman wringing out a hide . Owens valley pottery . Paiute dance corral . 39 26 . 42 27 . Woman with tattoed face . 43 44 45 45 48 59 69 28 . Women pla…”
- [ ] owensvalleyhistory/stories__some early history of owens river valley.pdf.pdf — KW #5 p3 · T2 none/none
  - “o kill them for eating. Fremont, on his journey to Sutter's Fort, ran into one of their strongholds, where the ground for acres was whitened with the bones of the horses …”
- [ ] owensvalleyhistory/stories__chronological_history_ov.pdf.pdf — KW #6 p2 · T2 none/none
  - “e on July 4 with the intention of keeping peace between the Paiutes and the settlers who were moving cattle on to the Indian lands. Alney McGee brought cattle from Tulare…”
- [ ] owensvalleyhistory/stories__allen_matlick_history.pdf.pdf — IX #1 0.0413 · KW #7 p2 · T2 none/none
  - “Allen Matlick History Page 2 There were Paiute Indians living along the Owens River and Bishop Creek. They were a friendly people and few incidents of friction occurred b…”
- [ ] owens-valley-paiute-autobiographies.pdf — IX #7 0.0014 · KW #10 p13 · T1 academic/mild
  - “steward] AN OWENS VALLEY PAIUTE 195 proposed peace and arranged a big feast at Fort Independence for all the Indians in the region. The Indians arrived, Panatiibiji' amon…”
- [ ] owensvalleyhistory/our_world2__page15.html.txt — IX #5 0.0015 · T2 none/none
  - “The rooms were furnished with army cots, straw mattresses and electricity. There were communal mess halls, laundry facilities and latrines. Sumiko Nakashima Ruth Takechi …”
- [ ] owensvalleyhistory/manzanar1__page11.html.txt — IX #11 0.0004 · T2 none/none
  - “ards, Though we saw no apple trees. Just the rows of prison barracks, With the barbed wire boundaries. Chorus: And we dream of apple blossoms Waving free beneath the star…”
- [ ] owensvalleyhistory/stories__The Ever-Changing World of the Paiute.pdf.pdf — IX #12 0.0004 · T2 none/none
  - “’ early creation histories all seem to stem from the same root. Another handed down early historic epic is that at one time all the people lived together in one large ban…”
- [ ] none

## 48. What role did alkali dust from dry Owens Lake play in regional environmental policy debates?

- [x] owensvalleyhistory/stories__keeping_dust_down.pdf.pdf — IX #1 0.9337 · KW #3 p1 · T2 none/none
  - “Keeping the dust down in California’s Owens Valley A civil engineer battles Los Angeles over its air pollution legacy. Jane Braxton Little March 2, 2015 Downdrafts kick u…”
- [ ] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — KW #1 p20 · T2 none/none
  - “15 POINTS OF INTEREST IN THE OWENS RIVER VALLEY Owens Lake is a 100 square mile alkali lake that famously dried up after the city of Los Angeles diverted the region's wat…”
- [ ] owensvalleyhistory/stories__owens_lake_land_use_REDUCED.pdf.pdf — IX #5 0.0014 · KW #2 p6 · T2 none/none
  - “protection and recreational use of the natural environment. Policy BIO-2.1 Coordination on Management of Adjacent Lands. Work with other government land management agenci…”
- [ ] owensvalleyhistory/owens_valley_owens_lake__page99.html.txt — IX #3 0.0077 · KW #4 · T2 none/none
  - “ittsburg Plate Glass Company plant on the western shores of Owens Lake at Bartlett - 2023 (Photo courtesy of Richard Bellomy) charcoal kilns on the western shores of Owen…”
- [ ] owensvalleyhistory/stories__a_lake_no_more.pdf.pdf — IX #2 0.068 · KW #5 p1 · T2 none/none
  - “1 A Lake No More Before diversions began, Owens Lake covered over 100 square miles of the Owens Valley floor. Steamships had once plied its water carrying silver bu…”
- [ ] fauna-flora-ov.pdf — IX #6 0.0012 · KW #6 p7 · T2 none/none
  - “is definitely a survivor. The Fish Slough Area of Critical Environmental Concern (ACEC) is one of the best places to view the pupfish. According to the Bureau of Land Man…”
- [ ] owensvalleyhistory/stories__death valley men_COMPRESSED.pdf.pdf — IX #4 0.0045 · T2 none/none
  - “ Lake. The chemical plants extract soda and allied salts from the thick saline solution which is Owens Lake. The lake is unbeautiful and the soda works, through which the…”
- [ ] owensvalleyhistory/stories__armstrong_why_owens_lake_is_red_1981.pdf.pdf — IX #8 0.0011 · T2 none/none
  - “Why Owens Lake is Red By Wayne P. Armstrong Desert Magazine – May 1981 One of nature's most remarkable biological phenomena is the pink and red coloration of salt lakes a…”
- [ ] owensvalleyhistory/stories__myth_history_and_water.pdf.pdf — IX #11 0.0007 · T2 none/none
  - “ the benefits of irrigation. But irrigation demanded water already on the ground, not waiting for it to fall from the sky. Meanwhile, some 250 miles to the north, another…”
- [ ] none

## 49. How did the completion of the aqueduct change land values and property ownership patterns in Owens Valley?

- [x] owensvalleyhistory/stories__police_ready.pdf.pdf — IX #4 0.9422 · KW #5 p5 · T2 none/none
  - “y at all times. OFFER REFUSED This offer was refused by the valley people, who asserted that nothing short of the purchase of all agricultural land in their district woul…”
- [x] owensvalleyhistory/stories__water_struggle.pdf.pdf — IX #5 0.8963 · KW #6 p4 · T2 none/none
  - “Valley of Broken Hearts – Part 2 4 They will even remind you, if the thought had not occurred to you, that for every acre brought under cultivation about the to…”
- [x] ov-native-water-story.pdf — IX #1 0.9866 · T1 primary_indigenous/none
  - “. Because they had stolen the rich soils of our homeland, we moved to the sites, we began to make homes in the areas we once lived on and became day laborers for the whit…”
- [x] owensvalleyhistory/stories__never_the_same.pdf.pdf — IX #2 0.9758 · T2 none/none
  - “Things Will Never Quite be the Same The City of Los Angeles quickly and quietly began the process of acquiring water rights through permits, condemnations and outright la…”
- [ ] owensvalleyhistory/stories__owens_lake_land_use_REDUCED.pdf.pdf — KW #1 p7 · T2 none/none
  - “sed project area as Natural Resources and State and Federal Lands.29 Lands adjacent to the lake bed are primarily flat, desert open space with sparse vegetation. The comm…”
- [ ] water-land-history-oviwc.pdf — IX #3 0.9577 · T1 primary_indigenous/none
  - “WATER & LAND HISTORY — Owens Valley Indian Water Commission A HISTORY OF WATER RIGHTS & LAND STRUGGLES Time Immemorial The Nüümü have lived in Payahuunadü “Land of the Fl…”
- [ ] owensvalleyhistory/stories__white_gold_disaster.pdf.pdf — KW #2 p1 · T2 none/none
  - “1 ‘WHITE GOLD’ CARRIES DISASTER TO PIONEERS OF OWENS RIVER VALLEY Here is the fifth of a series of dramatic fact stories of the tragedy that has overtaken the Owens River…”
- [ ] story-of-inyo.pdf — KW #3 p357 · T3 settler_bias/moderate
  - “LOS ANGELES AQUEDUCT 329 and its consummation will be local history of the first importance. This is written as a brief record, necessarily giving only the merest outline…”
- [ ] geology-and-water-resources-ov-report.pdf — KW #4 p76 · T3 institutional_bias/mild
  - “s (fig. 18). Therefore the distribution of field determined values of the aquifer hydraulic characteristics are concentrated in small areas near the well fields. A slight…”
- [ ] owensvalleyhistory/stories__chronological_history_ov.pdf.pdf — IX #7 0.8429 · T2 none/none
  - “ was in Robber's Roost, robbed stages and freight wagons along the eastern Sierra, especially near Coyote Wells (Freeman Junction) until he was captured later that year. …”
- [ ] owensvalleyhistory/ov_aqueduct__page19.html.txt — IX #9 0.7853 · T2 none/none
  - “ to be bought, bings the city into ownership of what they term "98 percent of the water bearing lands in Mono Basin." Practically the same small ration of lands remain pr…”
- [ ] owensvalleyhistory/stories__owens_2004_lores.pdf.pdf — IX #10 0.6993 · T2 none/none
  - “POINTS OF INTEREST IN THE OWENS RIVER VALLEY POINTS OF INTEREST IN THE OWENS RIVER VALLEY A Center for Land Use Interpretation publication The contents of this book are p…”
- [ ] none

## 50. Describe the oral traditions or storytelling practices of the Owens Valley Paiute people.

- [x] payahuunadu-oviwc.pdf — IX #1 0.9968 · KW #2 p3 · T1 primary_indigenous/none
  - “Our Ecology Prior to Western Contact The Nüümü (Owens Valley Paiute) are a people born of water. Our oral histories, passed down from generation to generation, tell of th…”
- [x] ethnography-of-owens-valley-paiute.pdf — IX #2 0.9912 · KW #4 p9 · T1 academic/mild
  - “Steward: Ethnography of Owen8s Valley Paiute TRIBAL DISTRIBUTIONS The Owens Valley Paiute are the southernmost of that widely dis- tributed Shoshonean group, the Northern…”
- [x] owensvalleyhistory/stories__The Ever-Changing World of the Paiute.pdf.pdf — IX #7 0.7527 · KW #1 p2 · T2 none/none
  - “homeland in which they dwelt. The tie between the people and the land was of such intimate bonding that it continues to remain a hurtful subject when our people remember …”
- [x] owensvalleyhistory/stories__northern paiutes of california and nevada.pdf.pdf — IX #6 0.759 · KW #3 p73 · T2 none/none
  - “SHORT LIST OF READINGS ON THE NORTHERN PAIUTE GENERAL DESCRIPTIONS Kelly, Isabel T. Ethnography of the Surprise Valley Paiute . University of California Publications in A…”
- [ ] owensvalleyhistory/bishop_residents2__page48cc.html.txt — IX #5 0.832 · KW #9 · T2 none/none
  - “Owens Valley Shoshone - Paiutes Owens Valley Paiute - Bishop, CA Owens Valley Shoshone - Paiutes Bishop - 5 Joe Bowers - Owens Valley Paiute (Courtesy J.D. Blac…”
- [ ] owens-valley-paiute-autobiographies.pdf — IX #4 0.8571 · T1 academic/mild
  - “SMITHSONIAN INSTITUTION Bureau of American Ethnology BuUetin 119 Anthropological Papers, No. 6 Panatiibiji', an Owens Valley Paiute By JULIAN H. STEWARD 183 PANATUBUr, AN…”
- [ ] owensvalleyhistory/stories__backroad tours in inyo county.pdf.pdf — KW #5 p5 · T2 none/none
  - “d needed resources, while others were quite settled; in the Owens Valley and Benton Hot Springs incipient agriculture is shown by irrigation used to enhance growth within…”
- [ ] water-land-history-oviwc.pdf — KW #6 p6 · T1 primary_indigenous/none
  - “surface water management practices. The Tribes’ current land base is woefully inadequate to meet the existing and future needs of the growing Nüümü population. Despite th…”
- [ ] owensvalleyhistory/independence__page69.html.txt — IX #9 0.57 · T2 none/none
  - “Pack Train heading up Kearsarge Pass Pack Train heading up Kearsarge Pass Snow covered Onion Valley Road Owens Valley - 1931 Snow covered Onion Valley Road Owens Valley -…”
- [ ] ov-native-water-story.pdf — IX #10 0.546 · T1 primary_indigenous/none
  - “Payahǖǖnadǖ Water Story – Wading Through the Past Teri Red Owl This is our water story of Payahǖǖnadǖ, our homelands. We interpret the name as being the place where water…”
- [ ] none

