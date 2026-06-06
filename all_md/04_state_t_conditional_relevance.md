|             | INTERNALRESEARCHDOSSIER |                         | • NOTFORDISTRIBUTION    |        |
| ----------- | ----------------------- | ----------------------- | ----------------------- | ------ |
|             | From                    | State                   | T to                    | the    |
| Conditional |                         | Relevance               |                         | Engine |
|             | TheoryChallenged        | → ArchitectureCorrected |                         |        |
| →           | MathematicsFormalised   | →                       | ImplementationReadiness |        |
AnInstitutionalResearchDossieronAdaptiveMeanReversion
InsideTrendyMarkets
|     | Programme: | AdaptiveMean-Reversion(AMR)Research |     |     |
| --- | ---------- | ----------------------------------- | --- | --- |
Layerfocus: L2Regime-ShiftDetection • Cross-LayerInformationRelevance
Documentclass: CompiledSynthesis—Adversarial,Reconciliation,Formalisation
Date: 31May2026
Thisdossiercompilesthreeresearchartifactsintoasinglecoherentwork:anadversarialoperationalization
study,aresearch-statereconciliation,andamathematicalformalizationofconditionalinformation
relevance.Itiswrittenfinance-first,quant-second.Allquantitativeclaimsremainprovisionaluntil
validatedonlocked-outdata;thedocument’spurposeistobridgeconvergedtheorytoanimplementable
engine,nottoassertafinishedresult.

| Document |     |     | Control | & Provenance |
| -------- | --- | --- | ------- | ------------ |
Thisdocumentisacompilation: aneditorialsynthesisofthreefrozen-or-convergingresearch
notesintooneinstitutionaldossier. Theresearchconclusionsarepreserved;thecontribution
hereisarchitecture,sequencing,notationdiscipline,andreadability. Nothingbelowreopens
settledtheoryorintroducesnewmethodology.
Roleinthisdossier
Sourceartifact
|               | Part I —        | adversarial | operationalization: | can the framework |
| ------------- | --------------- | ----------- | ------------------- | ----------------- |
| State T Oper- | survivereality? |             |                     |                   |
ationalization
(Red-Team)
|     | PartII—reconciliation: |     | giventhecritique,whatsurvivesand |     |
| --- | ---------------------- | --- | -------------------------------- | --- |
Research-State whereareweheaded?
Reconcilia-
tion & Open-
Methodology
Map
|                    | PartIII—formalization:   |     | howdowemathematicallydetermine |     |
| ------------------ | ------------------------ | --- | ------------------------------ | --- |
| Conditional Infor- | whichinformationmatters? |     |                                |     |
mation Relevance
Framework
Status legend used throughout. FROZEN (decided; do not reopen without strong new
evidence)• SPECIFIED — PRE-EMPIRICAL(fullydesigned,awaitingdata)• OPEN(genuinely
unresolvedattheimplementationlevel)• DIRECTION ACCEPTED(adversarialpivotadopted,
mechanicspending).
A note on notation. The three source notes used slightly different symbols for the same
objects. Thisdossierstandardisesthemonce, here, andusesthemconsistentlythereafter:
µ∗ (latent equilibrium price), ε = P−µ∗ (the residual / deviation), z (the standardised
deviation),z (entrythreshold), R /C /w (relevance,confidence,andconfidence-
| entry |     | i,t | i,t i,t |     |
| ----- | --- | --- | ------- | --- |
shrunkweightofinformationsourceiattimet). ThefullsymboltableisintheGlossary&
MathematicalAppendix.
1

Contents
DocumentControl&Provenance 1
Reader’sGuide 6
SynthesisOverview 7
I AdversarialOperationalizationofStateT 8
1 FromTheoreticalObjecttoMeasurableEdge 9
1.1 Howtoreadthispart,andwhatisnewinit . . . . . . . . . . . . . . . . . . . . 9
1.2 TheempiricalontologyofStateT . . . . . . . . . . . . . . . . . . . . . . . . . . 10
1.2.1 WhatobservableobjectdoesTcorrespondto? . . . . . . . . . . . . . . 10
1.2.2 Point,window,orprobabilistic? . . . . . . . . . . . . . . . . . . . . . . 11
1.2.3 Whatdoes“ignition”meanempirically? Fourobjects,ruthlesslysepa-
rated . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
1.2.4 WhatempiricalsignaturesshouldexistifTisreal?. . . . . . . . . . . . 12
1.3 Implementationtheory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
1.3.1 Thenaturalarchitecture . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
1.3.2 Theminimalviablearchitecture . . . . . . . . . . . . . . . . . . . . . . 13
1.3.3 Whatisprobablyoverengineering . . . . . . . . . . . . . . . . . . . . . 14
1.4 Economicsignificance . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
1.4.1 Whatmagnitudeactuallymatters,aftercosts . . . . . . . . . . . . . . . 14
1.4.2 Capacityandcrowding . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
1.4.3 WhichtrendstructuressupportT—themissingconditioninglayer . . 15
1.4.4 Whichmarketsandfrequenciestoprioritise . . . . . . . . . . . . . . . 16
1.5 Thecritical-speeding-upcritique . . . . . . . . . . . . . . . . . . . . . . . . . . 16
1.5.1 Thethreesignalsarenotthreeconfirmations—twoareonefact . . . . 16
1.5.2 Theoneindependentsignalisavolatilitysignal,notareversionsignal 17
1.5.3 Thechangeinκ isbelowthenoisefloorneartheunitroot . . . . . . . 17
1.5.4 IsCSUearly,oralaggingartifact? . . . . . . . . . . . . . . . . . . . . . 17
1.6 Thepressure-balancereformulation . . . . . . . . . . . . . . . . . . . . . . . . 17
1.6.1 Thereformulation,statedprecisely . . . . . . . . . . . . . . . . . . . . . 18
1.6.2 Whatqueuingtheorycontributes(theimplementablepart) . . . . . . . 18
1.6.3 Whatmean-fieldgamescontribute(theexplanatorypart) . . . . . . . . 19
1.6.4 Verdictonthepressure-balancereformulation . . . . . . . . . . . . . . 19
1.7 Empiricalresearchblueprint . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
1.7.1 Highest-valueunansweredquestions,ranked . . . . . . . . . . . . . . 20
1.7.2 Thecheapesthigh-informationexperiments . . . . . . . . . . . . . . . 20
1.7.3 Whattofreezenow,whattokeepflexible . . . . . . . . . . . . . . . . . 20
1.7.4 Thebiggesthiddenrisks . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
1.8 Finaladversarialverdict . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
2

AdaptiveMean-ReversionProgramme CONTENTS
EditorialBridge: FromCritiquetoReconciliation 23
II ReconciliationandtheCorrectedResearchState 24
2 Research-StateReconciliation&Open-MethodologyMap 25
2.1 Purposeandhowtoreadthis . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
2.2 Theframeworkasitactuallystands . . . . . . . . . . . . . . . . . . . . . . . . 25
2.3 Mission-to-statereconciliation . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26
2.3.1 Equilibriumestimation . . . . . . . . . . . . . . . . . . . . . . . . . . . 26
2.3.2 Information-relevancearchitecture . . . . . . . . . . . . . . . . . . . . . 27
2.3.3 MR-opportunityclassification. . . . . . . . . . . . . . . . . . . . . . . . 27
2.3.4 Regimedetection&structuralbreaks . . . . . . . . . . . . . . . . . . . 27
2.3.5 Real-worlddeployability . . . . . . . . . . . . . . . . . . . . . . . . . . 27
2.3.6 Thereconciliationinonematrix . . . . . . . . . . . . . . . . . . . . . . 27
2.4 Information-relevancearchitecture(thecenterpiece) . . . . . . . . . . . . . . . 28
2.4.1 Thediscipline: fivelessons . . . . . . . . . . . . . . . . . . . . . . . . . 28
2.4.2 Methodsevaluated . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
2.4.3 Therecommendedarchitecture . . . . . . . . . . . . . . . . . . . . . . . 29
2.5 Market-adaptiveinformationarchitecture . . . . . . . . . . . . . . . . . . . . . 30
2.5.1 Markettaxonomy . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30
2.5.2 Universalcorevs.market-specificmodules . . . . . . . . . . . . . . . . 31
2.6 Theremainingopenimplementationfrontier . . . . . . . . . . . . . . . . . . . 31
2.6.1 Thetrend-etiologyclassifier(method) . . . . . . . . . . . . . . . . . . . 31
2.6.2 Flow/pressure-balanceoperationalisation . . . . . . . . . . . . . . . . 31
2.6.3 Equilibrium-layeropenitems . . . . . . . . . . . . . . . . . . . . . . . . 31
2.6.4 Classification&integrationwiring . . . . . . . . . . . . . . . . . . . . . 32
2.6.5 Cross-sectionalformulation . . . . . . . . . . . . . . . . . . . . . . . . . 32
2.7 Datafeasibilityandoperationalconstraints . . . . . . . . . . . . . . . . . . . . 32
2.8 Routingtheexplorationintotheempiricalgate . . . . . . . . . . . . . . . . . . 33
2.9 Recommendationsandrankedroadmap . . . . . . . . . . . . . . . . . . . . . . 34
2.9.1 Immediatepriorities(highestROIfirst) . . . . . . . . . . . . . . . . . . 34
2.9.2 Whatisdeferred,andwhatshouldstopbeingresearched . . . . . . . . 34
2.9.3 Ifcodingstartedtomorrow: exactlywhatv0contains . . . . . . . . . . 35
EditorialBridge: FromArchitecturetoMathematics 36
III ConditionalInformationRelevance: TheMathematicalFormalization 37
3 TheConditionalRelevanceEngine 38
3.1 Executivesummary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 38
3.2 Framingthebottleneck . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39
3.2.1 Whythisisthehardpart . . . . . . . . . . . . . . . . . . . . . . . . . . . 39
3.2.2 Whatthisisnot . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39
3.2.3 Theobjectwearetryingtobuild . . . . . . . . . . . . . . . . . . . . . . 39
3.3 Whatdoes“mattering”mean? Definitionalwork . . . . . . . . . . . . . . . . . 39
3.3.1 Sixcandidatedefinitions . . . . . . . . . . . . . . . . . . . . . . . . . . . 39
3.3.2 Thecommitteddefinition . . . . . . . . . . . . . . . . . . . . . . . . . . 40
3

AdaptiveMean-ReversionProgramme CONTENTS
3.3.3 Themathematicalformofrelevance . . . . . . . . . . . . . . . . . . . . 40
3.4 Whatdoes“confidence”mean? . . . . . . . . . . . . . . . . . . . . . . . . . . . 40
3.4.1 Thefourdriversofconfidence . . . . . . . . . . . . . . . . . . . . . . . 41
3.4.2 Themathematicalformofconfidence . . . . . . . . . . . . . . . . . . . 41
3.4.3 Theoperationalcoupling: confidence-shrunkrelevance . . . . . . . . . 41
3.5 Whyrelevancemustevolve,andwhenitstops—thetheoreticalanchors . . . 42
3.5.1 AdaptiveMarketsHypothesis—whyrelevanceevolvesatall . . . . . . . 42
3.5.2 Time-varyingpredictabilityliterature—wheninformationstopsmattering 42
3.5.3 LópezdePrado—howtoavoidspuriousrelevance . . . . . . . . . . . . . 42
3.6 Candidatemathematicaltools—honestevaluation . . . . . . . . . . . . . . . 42
3.7 Thecommittedminimalframework(formalspecification) . . . . . . . . . . . 43
3.7.1 Inputstheengineassumes . . . . . . . . . . . . . . . . . . . . . . . . . . 44
3.7.2 Preprocessing: clustertodefeatsubstitution . . . . . . . . . . . . . . . 44
3.7.3 Step1—per-windowincrementalskill . . . . . . . . . . . . . . . . . . 44
3.7.4 Step2—adaptiverelevance(forgetting) . . . . . . . . . . . . . . . . . 44
3.7.5 Step3—thefourconfidencecomponents . . . . . . . . . . . . . . . . . 44
3.7.6 Step4—confidence-shrunkweightandaggregation . . . . . . . . . . 45
3.7.7 Theengineinpseudocode . . . . . . . . . . . . . . . . . . . . . . . . . . 45
3.7.8 Parametersandhowtosetthem(allinterpretable) . . . . . . . . . . . . 45
3.8 HowtheCREplugsintotheexistingstack . . . . . . . . . . . . . . . . . . . . . 46
3.9 Anti-overfittingandvalidationprotocol . . . . . . . . . . . . . . . . . . . . . . 47
3.10 Failuremodesandhonestlimitations . . . . . . . . . . . . . . . . . . . . . . . . 47
3.11 Implementationroadmap(minimumviableenginefirst) . . . . . . . . . . . . 47
3.12 Openquestions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 48
3.13 Closing—didwemeetthesuccesscriterion? . . . . . . . . . . . . . . . . . . . 48
IV Glossary&MathematicalAppendix 49
A Glossary&MathematicalAppendix 50
A.1 Symboltable . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 50
A.2 Formulaglossary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 51
A.2.1 Theresidual(thetradedobject) . . . . . . . . . . . . . . . . . . . . . . . 51
A.2.2 AR(1)varianceidentity—theCSUdouble-countingproof . . . . . . . 52
A.2.3 Netpressureandtheignitioncondition . . . . . . . . . . . . . . . . . . 52
A.2.4 Incrementalskill(theatomofrelevance) . . . . . . . . . . . . . . . . . 52
A.2.5 Relevancerecursion(adaptivity) . . . . . . . . . . . . . . . . . . . . . . 52
A.2.6 Confidence(multiplicativetrust) . . . . . . . . . . . . . . . . . . . . . . 52
A.2.7 Confidence-shrunkweightandaggregation . . . . . . . . . . . . . . . 53
A.2.8 Costedtriple-barrierlabelandtheeconomichurdle . . . . . . . . . . . 53
A.3 Methodologyglossary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 53
A.3.1 AnchoredKalmanfilter(equilibriumestimation,µ∗) . . . . . . . . . . . 53
A.3.2 MRScore/DRC(Layer1detection) . . . . . . . . . . . . . . . . . . . . 53
A.3.3 Trend-etiologyclassifier(themissinglayer) . . . . . . . . . . . . . . . . 54
A.3.4 Discrete-timehazard/survivalpanel+meta-labelling . . . . . . . . . 54
A.3.5 Pressure-balancereformulation(orderflow,queuing,MFG) . . . . . . 54
A.3.6 Elastic-netshrinkagetowardaneconomicprior(staticrelevanceback-
bone) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 54
A.3.7 Partialpooling/hierarchicalshrinkage(regimeconditioning) . . . . . 55
4

AdaptiveMean-ReversionProgramme CONTENTS
A.3.8 Stabilityselection(confidencecomponent) . . . . . . . . . . . . . . . . 55
A.3.9 Bayesianonlinechangepointdetection(BOCD,conditioning) . . . . . 55
A.3.10 Information-theoreticscreens(CMI,transferentropy)—cross-check
only . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 55
A.3.11 Excludedmethods(namedtoclosethemoff) . . . . . . . . . . . . . . . 55
A.4 Key-conceptglossary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 55
A.5 Theempiricalgateataglance . . . . . . . . . . . . . . . . . . . . . . . . . . . . 58
B ConsolidatedReferences 59
ConsolidatedReferences 59
5

Reader’s Guide
Whatthisdossieris. TheAdaptiveMean-Reversion(AMR)programmeseeksanarrowbut
genuineedge: totrademeanreversioninsidemarketsthatlookstructurallytrendy,byrecognising
when a reversion regime is forming before the broader market prices it in. The programme is
organisedinfivelayers—detection(Layer1),regime-shiftdetection(Layer2),equilibrium
estimation(Layer3),marketclassification(Layer4),andsignalgeneration(Layer5). This
dossierconcernsthelivefrontier: hardeningtheLayer-2objectcalledStateT,andbuilding
thecross-layermachinerythatdecideswhichinformationthesystemshouldlistento.
Thenarrativearc. Thethreepartsaresequencedsothatareaderunfamiliarwiththeproject
canfollowthelogicendtoend:
1. PartI—AdversarialOperationalization. WetakethefrozentheoryofStateTasgiven
andtrytokillitsoperationalform. Whereitsurvives,wesayexactlywhy;whereitfails,
weproposethenarrowestversionthatstilllives. Thispartreadsas: “Cantheframework
survivereality?”
2. PartII—Reconciliation&CorrectedResearchState. Thecritiquemateriallychanged
severalassumptions. Herewereconcilethecontradictions,stateplainlywhatsurvived
and what was revised, and lay out the corrected architecture and roadmap. This part
readsas: “Giventhecritique,whatactuallysurvives,andwhereareweheaded?”
3. PartIII—ConditionalInformationRelevance. Thereconciliationidentifiesinformation
relevanceasthelastconceptualbottleneckbeforesoftware. Thispartformalisesitmathe-
matically—definingwhatinformationmatters,whenitmatters,andhowconfidentwe
are—andcommitstoasingleimplementableengine,theConditionalRelevanceEngine
(CRE).Thispartreadsas: “Howdowemathematicallydeterminewhichinformationmatters?”
Itistheculmination: thebridgefromresearchtoimplementation.
Thedossierinonesentence
TheflagshipstatisticalsignatureofStateTdoesnotsurviveadversarialscrutinyand
must be demoted; the decisive missing variable is why the current trend exists (trend
etiology); and the unifying machine that ties detection, equilibrium-selection, and
early-warningintoonequestionisadisciplined,confidence-shrunkconditionalrelevance
engine. Theorywaschallenged,thearchitecturewascorrected,andthemathematicsis
nowformalisedandimplementation-ready.
Operatingphilosophy(inheritedandpreserved). Simple→interpretable→robust→useful
before complex → elegant → fragile; out-of-sample over in-sample; economic significance
overstatisticalsignificance;and“stoppingisasuccessfuloutcome.” Nothinginthisdossier
relaxesthosecommitments. Mathematicssupportsthenarrative;itdoesnotdominateit.
How to read selectively. A reader pressed for time should read this guide, the synthesis
overviewthatfollows, theverdictboxesineachpart, thestatusmatrixinPartII,andthe
committed specification in Part III. The Glossary & Mathematical Appendix makes the
documentself-contained: everyformula,methodology,andkeyconceptisexplainedthere
fromfirstprinciples.
6

Synthesis Overview
Thethreepartsarenotindependentessays;theyarethreemovementsofoneargument. The
table below is the spine of the whole dossier — the through-line a reader should keep in
mind.
| Movement | Centralmove                   | Whatchangesdownstream           |     |
| -------- | ----------------------------- | ------------------------------- | --- |
|          | Demotethecritical-speeding-up | Thedetectorisrebuiltaround      |     |
| PartI    | signaturefromidentitytoweak   | flowandcrowding,notaround       |     |
|          | diagnostic;promotetheorder-   | anear-unit-rootstatistic;aneti- |     |
|          | flow/pressure-balanceobject   | ologygatebecomesmandatory.      |     |
toprimary;exposetrendetiol-
ogyasthemissingconditioning
variable.
|     | Reconcilewhichlayersare | Av0architectureemerges: | a   |
| --- | ----------------------- | ----------------------- | --- |
PartII frozen,specified,oropen;iso- universalcoreplusthinmarket-
|     | lateinformationrelevanceasthe  | specificmodules,validatedonly |     |
| --- | ------------------------------ | ----------------------------- | --- |
|     | highest-leverageunsolvedprob-  | onout-of-sampleeconomic       |     |
|     | lem;makedatafeasibilityafirst- | value.                        |     |
classgate.
|     | Formaliserelevanceandconfi- | Detection,equilibrium- |     |
| --- | --------------------------- | ---------------------- | --- |
PartIII
|     | denceastwodistinctnumbers,  | selection,andearly-warning   |     |
| --- | --------------------------- | ---------------------------- | --- |
|     | fusedintoaconfidence-shrunk | collapseintoonemathematical  |     |
|     | weight;committotheCondi-    | questionthesoftwarecanevalu- |     |
|     | tionalRelevanceEngine.      | ateeachtimestamp.            |     |
Thereaderwillnoticeadeliberateconvergence: PartIarguesoneconomicandmicrostructural
groundsthatflowandcrowdingmattermorethanelegantresidualstatistics;PartIIshows
thedataeconomicspointtothesametwoaxes;andPartIIIsuppliesthemathematicalobject
— conditional, incremental, out-of-sample, confidence-weighted relevance — that makes
“which axis matters now” a computable quantity. Three independent lines of reasoning
arriveatthesameplace. Thatconvergenceisthedossier’scentralclaimtocredibility.
7

Part I
| Adversarial | Operationalization | of State |
| ----------- | ------------------ | -------- |
T
8

CHAPTER1
From Theoretical Object to Measurable
Edge
Layer2—Regime-ShiftDetection. Red-team/operationalizationpass.
Status: RESEARCH(ADVERSARIAL). Thispartdoesnot reopenthefrozentheory. Itassumesthefrozen
definition,ontology,mechanismset,andgate,andasksonequestionthefrozendocumentsdeliberately
didnotfinishanswering: canStateTbeturnedintoanempiricallymeasurable,economicallymeaningful,
implementableobject—andwhere,specifically,willthattranslationbreak?
Posture: prosecutorial. Thejobistotrytokilltheoperationalformofthethesis. Whereitsurvives,say
exactlywhy. Whereitfails,proposethenarrowestversionthatmightstilllive.
1.1 Howtoreadthispart,andwhatisnewinit
ThethreefrozenStateTdocumentsareunusuallyself-criticalforaninternalresearchartifact.
Theyalreadycontainanadversarialpass,anillusion-riskranking,afalsificationtable,and
pre-registeredkillcriteria. Aredteamthatmerelyre-listedthosewouldaddnothing. This
partisthereforescopedtothegapsthefrozenworkleftopenorgotwrong,anditmakes
sevenclaimsthefrozendocumentsdonotmake.
1. The flagship signature is the weakest leg, not the strongest. “Critical speeding up”
(CSU:κ↑,AR(1)↓,variance↓)ispromotedinallthreefrozendocstotheidentityofStateT.
Three of its components are not three independent confirmations — they are, to first
order,onefactstatedthreetimes—andthegenuinelyindependentpiece(innovation
variance)isavolatilitysignal,notamean-reversionsignal. Neartheunitrootthechange
inκ onwhichtheconstructrestsisbelowtheestimationnoisefloor(§1.5). Consequence:
demote CSU from identity to weak confirmatory diagnostic, and promote the order-flow
objecttoprimary.
2. There is a missing layer: trend etiology. State T is a flow-exhaustion / inventory-
completion phenomenon. It can therefore exist only in trends whose driver is flow or
positioning—notintrendsthataregenuineinformationrepricing,wheretheequilibrium
itselfmovedandthereisnothingtorevertto. Thefrozenframeworkconditionsonwhether
amarkethashistoricallybeenmean-reverting(MRScore)butneveronwhythecurrenttrend
exists(§1.4). Thisisthesinglemostconsequentialomission.
3. The frozen gate has two design flaws that can pass an artifact. Test P1 as written
conditionsontheoutcomeandconfirmsCSUbyconstruction;TestP3testssensitivity,but
theµ∗-lagillusionisasystematicbiasthatsurvivessmallperturbationsandistherefore
invisibletoP3asspecified(§1.7). Botharefixable;neitherisfixedinthecurrentspec.
4. “Reversion”isfournestedobjects,andtheprojectroutinelyletstheouteronesmasquer-
adeastheinnerone(§1.2).
9

AdaptiveMean-ReversionProgramme FromTheoreticalObjecttoMeasurableEdge
5. Thenaturalimplementationisadiscrete-timehazard/survivalpanel—notanHMM,
notRL,notdeeplearning—andtheminimalviablesystemissmallerthaneventhefrozen
“≤ 5-axisconjunctivegate”(§1.3).
6. Theeconomic-significancebarisquantifiablenow,anditishigh. Aback-of-envelope
forcesalow-single-digit-bps-per-tradehurdleatabaserateabove∼5%,whichmakesthe
strategycapacity-lightandcrowding-fragileinaspecific,estimableway(§1.4).
7. Thepressure-balancereformulationisthestrongestreframingavailable—anditis
the order-flow object, not a new one. Mean-field games and queuing theory give the
existingorder-flowmechanismarigorousgenerativemodel,ahazard,andareasonthe
recognitiongapexists. Theybelonginthegenerative/validationlayer,notthereal-time
stack(§1.6).
IfonlyonethingistakenfromPartI
Thefrozenframeworkisbuiltarounditsmostfragileobservable(CSU)andismissing
itsmostdecisiveconditioningvariable(trendetiology). Swaptheemphasis: leadwith
flowandetiology;treatthecritical-speeding-upsignatureasanoisyecho.
1.2 TheempiricalontologyofStateT
Thefrozenontologyislatenttransitionwindow→thresholdbifurcation→criticalspeedingup
→ hazard schedule → order-flow flip. That is a coherent conceptual ontology. It is not yet an
empiricalontology,becauseitdoesnotsaywhatsingleobjectyouwouldpointatinadatafile
andcall“T.”Thissectionsuppliesthat—andarguesthefrozendocspointedatthewrong
object.
1.2.1 WhatobservableobjectdoesTcorrespondto?
Thehonestfirst-principlesanswerseparatesthegeneratingobject,theobservableproxy,
andtheestimand.
▶ Generatingobject(latent). Asignchangeinthenetpressureontheresidual—thedrift
of ε = P−µ∗. In State A the residual’s drift, conditional on a deviation, points away
from µ∗ (continuation); in T it points toward µ∗ (reversion). T is the neighbourhood of
thezero-crossingofconditionalresidualdrift: athreshold-activateddriftsignchange,
observedastheonsetofanepisodic,clusteredprocess,whosecompletionisahazard.
▶ Observableproxy. Herethefrozendocsandthispartpartcompany. Thefrozendocs
makethestatisticalsignatureoftheresidual(κ,AR(1),variance)theprimaryobservable.
Thecorrectprimaryobservableisthenetorder-flow/pressureimbalanceanditsdrift,
because (i) it is the generating object’s most direct shadow, (ii) it does not require esti-
matinganear-unit-rootparameter,and(iii)ithasdocumented,model-lightprice-impact
structure(Cont–Kukanov–Stoikov2014: pricechange≈OFI/depth). Theresidualsta-
tisticalsignatureisaderived,lossy,estimation-fragilefunctionofthisobject,nottheobject
itself.
▶ Estimand. The conditional probability that a stretched residual (|z| ≥ z ) reverts
entry
enough to clear costs within horizon H, and the conditional probability that this is
happeningwhilepositioningislight. Everythingtheprojectcantestreducestothesetwo
conditionalprobabilitiesandtheirlead–lag.
10

AdaptiveMean-ReversionProgramme FromTheoreticalObjecttoMeasurableEdge
Verdict(1A).T’sempiricalobjectisathreshold-activatedsignchangeinconditional
residual drift, carried by an order-flow pressure flip, manifesting as an episodic
clusteredprocesswithahazard-governedduration. Itscleanestobservableproxyis
order-flowimbalanceanditsdrift,nottheresidual’scritical-speeding-upsignature.
Thefrozenframeworkmislabelledthelossyderivedstatisticastheidentity.
1.2.2 Point,window,orprobabilistic?
Thefrozenanswer(“window”)isrightbutincomplete. Threedistinctthingsareconflated
under“window”: (1)thelatenttransitionisawindowinthesenseofpositiveduration—the
driftdoesnotflipinstantaneously;(2)thedecisionobjectisapoint—ateachbaryoueither
enteroryoudonot,soyoutradeatimestampinsidethewindow,never“thewindow”;(3)
thethingyoucanactuallyestimateisneither—itisaprobabilityfieldoverbars(thehazardof
beinginorenteringT),becausetheunderlyingdriftsignislatentandestimated.
Thisthree-waysplithasahardconsequence: “measurethewidthofthewindow”isnot
directlyestimable,becausethewindowhasnoobservableedges—onlyaprobabilitythat
risesandfalls. Theearlinessgapmustberedefinedasalead–lagbetweentwoestimated
probabilityseries— P(reversionfiring)versus P(crowded)—notasameasuredduration.
Verdict (1B). Generatively a window; operationally a sequence of point decisions;
empiricallyaprobabilityfield. “Tiswindow-like”istruebutuntradeableasstated;
the tradeable form is a hazard / probability, and the earliness gap is a lead–lag of
probabilities,notawidth.
1.2.3 Whatdoes“ignition”meanempirically? Fourobjects,ruthlesslyseparated
This is the most important subsection in this section, because the project’s central self-
deceptionriskliveshere. Therearefourdistinctobjects,nested,andtheframeworkrepeat-
edlyletsanouteronestandinforaninnerone:
Thefour-objectnesting
(1)Statisticalreversion ⊃ (2)Economicallytradeablereversion ⊃ (3)Early(State-
T) reversion; and orthogonal to all three, (4) a successful fade event is an ex-post
realization,notastate.
▶ (1)Statisticalreversion— ε shrinksinexpectation: E[∆ ε·sign(ε)] < 0conditionalon
|z| ≥ z . Necessaryandalmostfreetofind. Finding(1)provesnothingtradeable.
entry
▶ (2)Economicallytradeablereversion—thecostedfadehaspositiveexpectancy: E[netfadeP&L] >
hurdle. Thisis(1)minusspread,slippage,roll,andthecostofstop-outswhenthedevi-
ationwidens. Thegapbetween(1)and(2)islargeandiswheremostcandidateedges
die.
▶ (3) Early / State-T reversion — (2) holds while positioning is still light, i.e. before the
crowdedStateB.Thisistheonlyobjectthatcarriesalpharatherthanbeta-of-reversion. It
requiresthenon-monotonecrowdingaxistoevenbedefined.
▶ (4) A successful fade event — a single realized trajectory in which a fade made money,
contaminatedbyluck. Conditioninganysignaturestudyon(4)isaselectiontrap: of
coursetheresidualreverted—thatiswhyitisinthe“successfulfade”set—andreversion
11

AdaptiveMean-ReversionProgramme FromTheoreticalObjecttoMeasurableEdge
mechanically produces AR(1)↓ and variance↓ ex post. A signature measured “around
historicaltradeable-fadeclusters”(thewordingoffrozenP1)isthereforeguaranteedto
“confirm”CSUregardlessofwhetheranyregimeexists.
Thedisciplinethisimposes: everytestmustbestatedasanas-of-decision-timediscrimi-
nation—doesanobservablecomputedonlyfromdatauptotseparatebarsthatwillbein
object(3)frombarsthatwillnot—andneveras“whatdoesthesignaturelooklikearound
thewinners.”
Verdict (1C). “Ignition” = the onset of object (3): the conditional-drift sign change
producingtradeablereversionwhilecrowdingislow. Theframework’smainfailure
modeismeasuringobject(1)onsample(4)andreportingitasevidenceforobject(3).
Thefour-waynestingmustbewrittenintothepre-registrationasthedefinitionofwhat
eachtestisandisnotallowedtoconditionon.
1.2.4 WhatempiricalsignaturesshouldexistifTisreal?
Statedasfalsifiable,signed,as-of-decision-timepredictionsacrossfivedatalayers. IfTis
realandearly,alloftheseshouldhold;theabsenceofanyoneisinformative.
|       | StateA(trend) | InsideT(ignition) | StateB    | Whythissign/    |
| ----- | ------------- | ----------------- | --------- | --------------- |
| Layer |               |                   | (crowded) | earliestobserv- |
able
continuation- OFIdriftcrosseszero; contrarianflow thecauseandthe
Orderflow aggressorshare aggressorshareflips numerous,two- earliestobserv-
|     | high;OFIsign= | contrarian;absorption | sided | able;leadsprice  |
| --- | ------------- | --------------------- | ----- | ---------------- |
|     | trendsign     | rising                |       | levelbyconstruc- |
tion
|          | εnearunit-root; | κrisingweakly,AR(1) | κhigh,stable | derived,lossy; |
| -------- | --------------- | ------------------- | ------------ | -------------- |
| Residual | / AR(1)≈1       | easing—butlagging   |              | thelastthingto |
| price    |                 | andnoisy            |              | confirm        |
|          | rangeexpanding/ | realizedrangeandσ   | low,stable   | asymptomofbal- |
contractingaroundµ∗
| Volatility | steady |     |     | ance,confounded |
| ---------- | ------ | --- | --- | --------------- |
withthevariance
legofCSU
|     | OIbuildingwith | OIbuilddecelerating | OIhigh,range | thenon- |
| --- | -------------- | ------------------- | ------------ | ------- |
Positioning thetrend /rangecontracting established monotonesep-
|     |     | whileOIflat |     | arator;defines |
| --- | --- | ----------- | --- | -------------- |
“early”
|         | trendcohortco- | thename’sresidual | reversioncohort | decoupling-     |
| ------- | -------------- | ----------------- | --------------- | --------------- |
| Cross-  | moving         | decouplesfromthe  | co-moving       | before-cohortis |
| section |                | cohortfirst       |                 | acleanearliness |
proxy;under-
exploited
Two signatures here are not in the frozen docs and are higher-information than CSU:
theOFI-driftzero-crossing(theliteralcause)andcross-sectionalresidualdecoupling(an
earlinessproxythatsidestepstheneedtoestimateκ atall). Thefrozendesignissingle-asset
andthereforecannotseethesecond—adesignlimitationworthrelaxing.
12

AdaptiveMean-ReversionProgramme FromTheoreticalObjecttoMeasurableEdge
1.3 Implementationtheory
AssumeTexistsinobject-(3)form. Whatsystemactuallyemerges? Thefrozendocsdefer
thisto“Stage3: ≤ 5-axisconjunctivegate+low-capacitymeta-label.” Thatisroughlyright
butunder-specifiedand,inonerespect,stilltoolarge.
1.3.1 Thenaturalarchitecture
Map the empirical object to the model class that fits it with the least imposed structure.
Theobjectisanepisodic,clustered,hazard-governedonsetwithacensoredduration(the
trendcanresume;Tnevercompletes)andcovariates(theprecursors). Thetextbookhomeof
“time-varyingprobabilityofanonsetevent,withcovariates,andcensoring”isdiscrete-time
survival/hazardmodelling—operationallyapooledpanellogisticregressionoftheevent
indicatoronas-of-timecovariates,withhazard
h(t | x
t
) =
P(cid:0)
enterobject-3att
(cid:12)
(cid:12)notyet, x
t
(cid:1)
.
This is deliberately humble: interpretable, native to censoring and low base rates, and it
producesacalibratedprobability(whichsizingneeds). Wrapitinmeta-labelling(Lópezde
Prado): aprimaryrulefirescandidatefades(|z| ≥ z withtherightsignvs.trend);the
entry
hazardmodelisthesecondarymodelthatsaystrade/don’ttradeandhowconfident.
Rejectedastheprimaryengine. FullHMM(modelsT’sinteriorasazero-widthjump
—wrongobject);reinforcementlearning(event-starved—hundreds,notmillions,of
independentepisodesatdailyfrequency;itwillmemorisethepath);deepsequence
models (same data-starvation, and they destroy the interpretability the charter de-
mands);continuous-timefilteringofκ (re-importstheestimationproblemof§1.5asa
state). Bayesianfilteringhasexactlyonelegitimaterole: atwo-statefilteronthedrift
signoftheimbalance/residual(notonκ),feedingthehazardmodelasonecovariate.
Verdict(2A).Discrete-timehazard(pooledlogistic)onas-of-timecovariates→meta-
label trade / no-trade → costed sizing. One optional two-state drift-sign filter as a
covariate. Everythingmoresophisticatedis,atthisdataregime,variance-fitting.
1.3.2 Theminimalviablearchitecture
The frozen docs pre-register five axes (κ-complex, timescale S, crowding C, balance B,
nonlinearactivationa). Foraminimalfirstsystemthatcanfalsifyitself,threeofthosefiveare
redundantorfragile. Theminimalviabledetectoristwogatesandonelabel:
1. A deviation gate — |z| ≥ z with sign(ε) opposed to the trend (the fade-strength /
entry
buy-the-dipcondition;asymmetricbyconstruction).
2. Acrowdinggate—thenon-monotonerecognitionaxis(OIbuildvs.rangecontraction).
This is the only axis that distinguishes object (3) from State B and is therefore non-
negotiableeveninv0.
3. Acostedtriple-barrierlabel(C3)—thefrozenprimarytarget,usedtobothtrainand
scorethehazard.
Deliberately excluded from v0: the κ-complex (M1), timescale separation (M2), bal-
ance/auction(M4),nonlinearactivation(M5). Theyareexcludednotbecausetheyarewrong
13

AdaptiveMean-ReversionProgramme FromTheoreticalObjecttoMeasurableEdge
butbecauseM1/M2/M5allderivefromthesamenear-unit-rootκ estimateandaddlittle
independentinformation,andav0thatalreadyneedsacrowdingaxisshouldprovethatone
decisiveaxiscarriesinformationbeforeaddingfourfragileones.
Thebindingconstraint
Theproject’sbindinginputisflow/positioningdataquality,notstatisticalsophisti-
cation. Ifthecrowdingaxiscannotbemeasuredcleanlyatthechosenfrequency,the
projectisoverbeforeanymodellingbegins. SpendthefirstweekondatafeasibilityofOI
/positioning/flow,notonestimators. Ifthetwo-gatev0cannotbeatitsblock-bootstrapnull,
nofive-axisversionwill.
1.3.3 Whatisprobablyoverengineering
Inpriorityorder: criticalspeedingupastheidentity(§1.5;highestrisk—threecoupled
statistics, two of which are one statistic, estimated where estimation is worst); timescale
separationSasaliveaxis(S = τ /half-lifeisaratiooftwonear-unit-rootestimates;keepas
µ
aconceptualnecessarycondition,donotcomputeitasafeatureinv0);nonlinearactivation
a (data-hungry;defer);theC3↔C4agreementcheckasaStage-1deliverable(runC3alone
t
inv0);and“fivemechanismsonthreeorthogonalsources”(M1,M2,M5allfunnelthrough
κ;theeffectivenumberofindependentaxesisclosertotwo—aκ/price-dynamicsaxisanda
flow/positioningaxis—plusvolatilityasaconfound).
Notoverengineering,andtobeprotected: thecrowdingaxis,thecostedmodel-freelabel
(C3), purged/embargoed CV, sample-uniqueness weighting, and the pre-registered kill
criteria. Thosearetheload-bearingdiscipline.
1.4 Economicsignificance
Thefrozendocsasserttheeffectis“small,capacity-limited,episodic”butneverquantifythe
bar. Hereisthebar.
1.4.1 Whatmagnitudeactuallymatters,aftercosts
Workitasahurdle,notahope,foradailyfadeonaliquidindexfuture. Round-tripfrictions
(conservative,liquidfuture)are∼3–6bps. Withapartial-reversionprofittarget g ≈ 0.5σRV
and a stop at deviation-widening s ≈ 1.0σRV, the per-trade payoff is asymmetric against
you (you risk ∼1.0σ to make ∼0.5σ). To be profitable net you therefore need a hit rate
comfortablyabove2/3onthegrossfade. IfσRV onadailybaris∼80–100bps,a0.5σpartial
reversionis∼40–50bpsgross;netof∼5bpsroundtripthatis∼35–45bpsperwinningtrade.
Meaningfulpertrade,butonlyifhitrateandbaseratehold.
Thenumbertokeepinfrontoftheproject
Theeconomic-significancefloorisroughlyanorderofmagnitudeabovethestatistical-
significancefloor. Areversionof5–15bpsthatisgenuineandstatisticallysignificant
isworthlessherebecauseitcannotcleara5bpsroundtripwithmargintosurvivethe
stop-outdistribution. Statisticalsignificanceisirrelevant;thequestioniswhetherrealizednet
partial-reversionclears∼5–6bpswithahitratethatsurvivestheasymmetricbarriergeometry.
14

AdaptiveMean-ReversionProgramme FromTheoreticalObjecttoMeasurableEdge
1.4.2 Capacityandcrowding
Ifobject(3)exists,itscapacityprofileisstructurallybadinaspecificway. Theedgeisthe
recognitiongap;themomentitiswidelytraded,thegapcloses—thisisnotarisk,itisthe
definition. Sothestrategyisself-extinguishingundercrowdingmoreaggressivelythana
typicalstat-arb. Capacityisboundedbyhowmuchcanbedeployedinsidethegapbefore
yourownflowbecomestherecognition.
Thehonestprioristhatthepublic-data,dailyversion
isthinpreciselybecauseitisnotsecret(theOI/low-crowdingreversalscreenispublished,
e.g.Quantpedia). Theedgeisepisodicandregime-specific;Sharpewillbelumpy,andthe
disciplinetonottradeinthewrongetiologymattersmorethansignalrefinement.
Verdict (3B). Real-but-small, capacity-light, self-extinguishing under crowding,
episodic. Consistentwithagenuinenicheedgeforamodestbook;inconsistentwitha
scalableinstitutionalstrategy. Sizetheambitionaccordingly.
1.4.3 WhichtrendstructuressupportT—themissingconditioninglayer
Thisisthemostimportantadditioninthissection,anditisabsentfromthefrozenframe-
work. StateT’smechanismisflowexhaustion/inventorycompletion. Thatmechanismpresup-
posesatrenddrivenbyfloworpositioning,notbyinformation.
|     | Stableµ∗torevert | Driverflow/inven- | DoesTplausiblyexist? |
| --- | ---------------- | ----------------- | -------------------- |
Trendetiology
|                     | to?           | tory(exhaustible)? |                           |
| ------------------- | ------------- | ------------------ | ------------------------- |
|                     | Yes—valueun-  | Yes—completion     | Stronglyyes.Textbookcase. |
| Inventory-imbalance | changed,price | forcesdealerrebal- |                           |
| trend               | pushedoffit   | ancing             |                           |
|                     | Mostly—flow-  | Yes—flowfiniteand  | Yes,andpartiallypre-      |
CTA/systematic-flow
|     | drivenovershoot | mechanical | dictable. |
| --- | --------------- | ---------- | --------- |
trend
|                      | Yes—pricede-    | Yes—theunwindis | Yes,butviolentandfat- |
| -------------------- | --------------- | --------------- | --------------------- |
| Speculativeblow-off/ | tachedfromvalue | thereversion    | tailed.               |
crowding
|     | Partially | Partly | Conditional—dependshow |
| --- | --------- | ------ | ---------------------- |
Momentumovershoot
farpastvalue.
(mild)
Driftingµ∗(carry
|                  |                | Partly          | Weak—theequilibrium    |
| ---------------- | -------------- | --------------- | ---------------------- |
| Carry-drivenmove | isarealreturn) |                 | itselftrends.          |
|                  | No—µ∗jumped    | No—information, | No.Noresidualtorevert; |
Macrorepricing(rates, notexhaustibleflow fadingthisisfightinginfor-
| policy,FX) |                      |                 | mation.       |
| ---------- | -------------------- | --------------- | ------------- |
|            | No—fundamen-         | No—physical,not | No/dangerous. |
| Commodity  | supply talvaluemoved | flow            |               |
shock
Thepatternissharp: Tlivesinflow/inventory/behaviouraltrendsandisabsent—ora
trap—ininformation-repricingandfundamental-shocktrends.
Threehardconsequences:
Apooledbaseratenearthefloor(∼5%)mighthide
1. Aggregationwashesouttheeffect.
a15%baserateininventorytrendsanda−5%“baserate”(systematiclosses)inmacro
repricing. Thebase-ratestudymustbestratifiedbyetiology,oritwillproduceafalsenegative.
2. A trend-etiology classifier is a missing required layer. Even a coarse 3-way split
15

AdaptiveMean-ReversionProgramme FromTheoreticalObjecttoMeasurableEdge
(flow/behaviouralvs.information-repricingvs.ambiguous),builtfromobservableprox-
ies,wouldgateouttheetiologieswhereTcannotexist. Thisismoredecisivethananyof
thefivestatisticalaxes.
3. MRScoredoesnotsubstituteforthis. MRScoreaskshasthismarkethistoricallyreverted—
aslow,unconditional,instrument-levelproperty. Etiologyisfast,conditional,episode-level:
thesameinstrumentisfade-friendlyduringaninventorytrendandadeath-trapduring
amacrorepricing,inthesamemonth. Thetwoareorthogonalandbothneeded.
Verdict(3C).Conditiononetiologyorexpectafalsenegative. Addacoarseetiology
gate. Stratifyeverybase-rateandpredictabilitystatisticbyit.
1.4.4 Whichmarketsandfrequenciestoprioritise
Frequency: runtheexistencegateatdailyfirst(cheap,thedataexists),butpre-committo
intradayastheprimaryexpectedhome—thepressureflipisamicrostructureeventwhose
naturalclockisintraday. Instruments: prioritisewhereflow/positioningisobservableand
flow-driventrendsarecommon—indexfutures(NIFTY,ES)scorewellviaOIandoptions
positioning. Avoid,early,anythingdominatedbyscheduled-informationrepricing(front-
end rates around central-bank dates; FX around data). Cross-sectional vs. directional: a
cross-sectionalformulation(fadetheresidualthathasdecoupledfromitscohortwhilethe
cohortstilltrends)ismorecapacity-robust,partiallyhedgesetiologyrisk,andgivesaκ-free
earlinessproxy—astrongcandidatetheprojecthasnotconsidered.
1.5 Thecritical-speeding-upcritique
ThefrozendocsmakeCSU(κ↑,AR(1)↓,deviation-variance↓)theidentityofT.Thissection
arguesthatistheframework’sbiggesttechnicalmistake.
1.5.1 Thethreesignalsarenotthreeconfirmations—twoareonefact
ForastationaryAR(1)residual ε = ϕε +η withinnovationvariance σ 2,theuncondi-
|     |     | t+1 t | t   | η   |     |
| --- | --- | ----- | --- | --- | --- |
tionalvarianceis
σ2
η
|     |     | Var(ε) | = . |     | (1.1) |
| --- | --- | ------ | --- | --- | ----- |
1−ϕ2
Var(ε)
The AR(1) coefficient ϕ and are therefore the same quantity up to σ η . If ϕ falls
| (AR(1)↓, | = −lnϕ↑) |     |     | “AR(1) |     |
| -------- | -------- | --- | --- | ------ | --- |
κ with σ η fixed, the variance falls mechanically. falling and
deviationvariancecontracting”isnottwopiecesofevidence—itisonefact(ϕfell)reported
| twice. Verifiednumerically(stationaryvarianceforσ |     |     | = 1): |     |     |
| ------------------------------------------------- | --- | --- | ----- | --- | --- |
η
|     |     | ϕ(AR1) κ | = −lnϕ Var(ε) |     |     |
| --- | --- | -------- | ------------- | --- | --- |
|     |     | 0.98     | 0.020 25.3    |     |     |
|     |     | 0.90     | 0.105 5.26    |     |     |
|     |     | 0.70     | 0.357 1.96    |     |     |
|     |     | 0.50     | 0.693 1.33    |     |     |
κ andvariancemoveinperfectlockstepbyconstruction;theycarrythesameinformation.
16

AdaptiveMean-ReversionProgramme FromTheoreticalObjecttoMeasurableEdge
1.5.2 Theoneindependentsignalisavolatilitysignal,notareversionsignal
Theonlywaydeviationvariancecarriesinformationbeyondϕisthroughσ —theinnovation
η
variance. Butσ isvolatility,notmeanreversion. Sothe“deviation-variancecontracting”
η
legofCSUis,totheextentitisindependentatall,avolatility-compressiondetectorwearing
amean-reversioncostume. Holdtrueϕ = 0.90fixedandonlyshrinkinnovations:
Regime Trueϕ(reversion) ObservedAR(1) ObservedVar(ε)
A(σ =1.0) 0.90(unchanged) 0.902 4.57
η
B(σ =0.4) 0.90(unchanged) 0.917 0.93
η
Variancefell∼5×whilethemean-reversionparameterdidnotmoveatall. Apurevolatility-
compressionepisode—commonattheendoftrendsandinlow-volregimes—counterfeits
theCSUsignature.
1.5.3 Thechangeinκ isbelowthenoisefloorneartheunitroot
CSUisaboutκ rising( ∆ κ > 0)early. ButStateAsitsattheunitroot,exactlywhereκ isworst
estimated. Simulating2000windowsof60dailybars:
Trueϕ Trueκ Meanϕˆ Biasinϕˆ SD(κˆ)
0.98 0.0202 0.892 −0.088 0.083
0.95 0.0513 0.863 −0.087 0.093
Thestandarddeviationoftheκ estimate(∼0.08–0.09)islargerthanκ itself(∼0.02–0.05),
andthebiasisseveraltimesκ. Detecting ∆ κ overashortwindowisstatisticallyhopelessat
dailyfrequencyneartheunitroot. Thisisnotatuningproblem;itisintrinsic.
1.5.4 IsCSUearly,oralaggingartifact?
Putting it together, the accusations against CSU each land. Lagging confirmation: yes,
partially—bytheframework’sowncausalordering,CSUisthethirdthingtohappen,after
theflowflipandbandactivation. µ∗ constructionartifact: yes,anddangerously—alagging
µ∗ makesε = P−µ∗ revertasµ∗ catchesup,manufacturingAR(1)↓andvariance↓;critically
thisbiasissystematic,soitisnotcaughtbythefrozenP3small-perturbationtest. Estimator
illusionnearunitroot: yes. Post-hoc/selection: yesifmeasuredontradeable-fadeclusters.
Constructive verdict (§1.5). Do not discard CSU — discard its primacy. (1) Demote
CSUfromidentitytoweakconfirmatorydiagnostic—atmostasinglecovariate,never
three. (2)NeveruseAR(1)andvarianceasseparatefeatures—theyareone;ifyouuse
variance,useitasanexplicitvolatilitycontrol. (3)Replace“measure ∆ κ”with“measure
theflow-imbalancedriftsignchange”astheprimaryearlyobservable. (4)Ifyoukeep
aresidual-dynamicsaxis,preferamodel-freevariance-ratio/partial-reversionstatistic
overκ.
1.6 Thepressure-balancereformulation
CanStateTbereformulatedasalatentpressure-balancetransitionproblem,withsupportfrommean-
fieldgames(MFG)andqueuingtheory? Shortanswer: yes,anditisthestrongestavailable
17

AdaptiveMean-ReversionProgramme FromTheoreticalObjecttoMeasurableEdge
reformulation—butMFGandqueuingbelonginthegenerative/validationlayer,not
thereal-timeengine. Theydonotaddanewmechanism;theygivetheexistingorder-flow
mechanismarigorousskeleton,ahazard,andanexplanationforwhytherecognitiongap
exists.
1.6.1 Thereformulation,statedprecisely
Definethenetpressureontheresidualastheconditionaldriftofε: atadeviationofsizez,
let
b(z,t) =
E(cid:2)∆
ε
(cid:12)
(cid:12)ε, state
(cid:3)
. (1.2)
StateAisb·sign(ε) > 0(deviationspushedfurther—continuationdominates). StateT’s
ignitionisthezero-crossing b(z,t) = 0followedby b·sign(ε) < 0(reversiondominates).
“Pressurebalance”isliterallyb = 0;“ignition”isthesignchangeofnetpressureattheextremes.
Thisisthesameobjectastheempiricalontologyof§1.2,butnowasinglescalarfieldwitha
crispevent—farmoremeasurablethanathree-partstatisticalsignature. Thepressurehas
twocompetingsources,andTistheircrossover:
b vs. b .
cont rev
(cid:124)(cid:123)(cid:122)(cid:125) (cid:124)(cid:123)(cid:122)(cid:125)
∝rateofnewtrend-alignedaggressiveflow ∝contrarian/absorbingflow+forcedinventoryrebalancing
Bothare,inprinciple,directlyobservablefromorderflow. Youmeasurethecause,notalossy
downstreamstatisticoftheeffect.
1.6.2 Whatqueuingtheorycontributes(theimplementablepart)
Thelimitorderbookisaqueuingsystem. Threeconcretecontributions:
1. Areduced-formgenerativemodelofthepressureflip. Intheheavy-traffic/diffusion
limit,thenetqueueimbalancebehaveslikeadiffusionwhosedriftisexactlythenetpressure
b. State T = the drift of the imbalance diffusion crossing zero. This gives a simulator:
generatesyntheticflowwithaknown,controllablepressure-fliptime,runthedetectoron
it,andmeasurewhetheritfindstheflipbeforeprice-levelreversionisvisible. Thisisthe
singlemostvaluableuse—itteststheearlinessclaimagainstagroundtruththatdoesnot
existinrealdata.
2. Afirst-passagehazard—therigorousformof“ignitiontiming.” Thehazardofignition,
P(netpressureflipsatt | notyet), is a first-passage / level-crossing problem of the
imbalancediffusion,whichqueuingtheorysolvesanalytically. Ittellsyouthefunctional
form the hazard should take and which covariates (queue sizes, arrival / cancellation
rates)driveit.
3. Whydailyaliasesit. Queuedynamicshavecharacteristictimesofseconds-to-minutes;
the inventory price-pressure half-life is ∼1 day. A daily bar integrates over the entire
flipandseesonlytheoutcome,notthetransition. Thisistheformalreasontoprioritise
intraday.
Limit, stated honestly. Estimating a full queue-reactive model in real time is heavy
andneedsmessage-levelLOBdata. Donotputthequeuingmodelinthelivestack.
Useitasthesimulatorfortheearlinessground-truthtestandthesourceofthehazard’s
functional form. The live observable is a cheap reduced-form: signed order-flow
imbalanceanditsshort-horizondrift.
18

AdaptiveMean-ReversionProgramme FromTheoreticalObjecttoMeasurableEdge
1.6.3 Whatmean-fieldgamescontribute(theexplanatorypart)
MFGmodelsacontinuumofsmallagents,eachsolvinganoptimal-controlproblem,coupled
only through the aggregate (the mean field). Its application to trade crowding is direct
(Cardaliaguet & Lehalle 2018). The mapping is precise: the two agent populations are
trend-followers and mean-reverters; State T is the regime where the population’s Nash
equilibriumtipsfromcontinuation-dominanttoreversion-dominantaggregateflow,with
b = 0themean-fieldequilibriumconditionatthecrossover. Mostvaluably,therecognition
gap(thealpha)=theconvergencetimeofthemeanfield: crowdingisthemassofagents
migrating to the reversion control, and that migration is not instantaneous. This yields
a testable qualitative prediction: the gap should widen with cross-sectional dispersion in
participanthorizons/speedandnarrowasparticipationhomogenises.
Why MFG must stay out of the real-time engine: solving an MFG means solving
a coupled forward–backward HJB / Fokker–Planck PDE system, with no closed form,
heavyparameterisationofunobservableagentcostfunctionals,andseriousnumericalcost.
Its legitimate uses are all off-line: a source of falsifiable qualitative predictions about the
recognitiongap;aconsistencycheckonthegenerativesimulator;andaconceptualdiscipline
thatkeeps“crowding”definedasanequilibrium/massobject(bestproxiedbyOIchangeand
positioningdispersion,notOIlevel).
1.6.4 Verdictonthepressure-balancereformulation
|     | Role | Livestack? | Concretedeliverable |
| --- | ---- | ---------- | ------------------- |
Component
|     | Thecorrectprimaryidentityof | Yes | Redefineignitionasthe |
| --- | --------------------------- | --- | --------------------- |
Pressure-balance re- T—replacesCSU (conceptual OFI-driftzero-crossing
| framing (b-field, | sign | target) |     |
| ----------------- | ---- | ------- | --- |
change)
|              | Theliveobservableofthepres- | Yes | Aflow-imbalancecovari- |
| ------------ | --------------------------- | --- | ---------------------- |
| Reduced-form | OFI +                       |     | ate+itsshort-horizon   |
sureflip
| drift        |                            |             | driftsign              |
| ------------ | -------------------------- | ----------- | ---------------------- |
|              | Generativesimulator+hazard | No(offline) | Synthetic-ground-truth |
| Queuingmodel | form                       |             | earlinesstest;hazard   |
form
|                | Explains/parameterisesthe | No(offline) | Qualitativepredictions |
| -------------- | ------------------------- | ----------- | ---------------------- |
| Mean-fieldgame | recognitiongap            |             | aboutgapwidth;crowd-   |
ingasmass/migration
The reformulation survives and is recommended as the conceptual and generative
backbone,ontheexplicitconditionthattheheavymachinerystaysoffline. Itisstrictly
betterthantheCSUidentityontheproject’sowncriteria—directness, falsifiability,
economic grounding — and, via the simulator, it is the only route to an earliness
ground-truthtest.
1.7 Empiricalresearchblueprint
Aconcreteroadmapthatsupersedesthefrozen“locktarget/rungate”onlybyreordering
andaddingthemissingpieces. Itdoesnotreplacethefrozendiscipline(purgedCV,sample-
uniqueness,pre-registration,killcriteria),whichstands.
19

AdaptiveMean-ReversionProgramme FromTheoreticalObjecttoMeasurableEdge
1.7.1 Highest-valueunansweredquestions,ranked
1. Isthedaily,public-datatradeable-fadebaserateabovethecost-and-marginfloorwithin
therightetiologybucket? (Notpooled.) Everythingdieshereifno. #1byfar.
2. Doesaflow-imbalancedriftsignchangeleadtheprice-levelreversion,andbyhow
much? (Theearlinessgap,redefinedasalead–lagofprobabilities.) Thealphaquestion,
askedoftherightobservable.
3. Doesthecrowdingaxisseparateobject-(3)fromStateB?(FrozenK4—stilldecisive.)
4. Is the apparent reversion toward a contemporaneous equilibrium, or µ∗ catch-up?
(Testedcorrectly—notviasmallperturbations.)
5. DoesCSUaddanythingbeyondflow+crowding? (Worthconfirmingsotheaxiscan
bedropped,notcarried.)
6. Atwhatfrequencydoesthepressureflipstopbeingaliased? (Queuingprior: intraday.)
1.7.2 Thecheapesthigh-informationexperiments
Inascendingcost,eachcapableofkillingorsharplyupdatingthethesis:
Whatitfalsifies
ID Experiment
WhethercleanOI/positioningandaflowproxy
E0 Datafeasibility(days) existatcandidatefrequencies. Runfirst;itisthe
truegate.
“Texiststradeablyatdaily”perbucket;converts
E1 Etiology-stratified base alikelyfalsenegativeintoarealsignal.
rate(1wk)
WhethereventsareIID—ifso,stop.
E2 Clustering(days)
Whether the earliness estimator can work, on
E3 Synthetic earliness queuing-simulatedflowwithaknownfliptime.
ground-truth (1 wk, Newandhigh-value.
offline)
WhethertheOFI-driftsignchangeleadsposition-
E4 Flow lead–lag on real ingbuild-up. ReplacesCSU-basedP2.
data(1–2wk)
ThecorrectedversionofP3.
E5 Acausal-µ∗ construction
test(days)
1.7.3 Whattofreezenow,whattokeepflexible
Freezeimmediately: thefour-objectconditioningrules(everytestisanas-of-decision-time
discrimination;nothingconditionsonrealizedfadesuccess);thecorrectedµ∗-construction
test(replace“smallperturbationsofasinglefrozenµ∗”withcomparisonagainststructurally
differentandacausalbenchmarks,becausetheµ∗-lagillusionisasystematicbiasinvisibletosmall
perturbations);thepressure-balanceframingastheidentitywithOFI-driftastheprimary
20

AdaptiveMean-ReversionProgramme FromTheoreticalObjecttoMeasurableEdge
earlyobservable;andtheetiologygateasarequiredconditioninglayer. Protectthecorrect
frozendisciplines: purged/embargoedCV,sample-uniquenessweighting,costedC3label,
pre-registerednumerickillcriteria,lockedhold-out,“stoppingisasuccessfuloutcome.”
Keepflexible: frequency(dailyvs.intraday,intradaytheexpectedhome);single-assetvs.
cross-sectional;theexactcrowdingproxy(OIchangevs.positioningdispersionvs.options
skew—MFGarguesformass/migration,notlevel);whichsecondaryaxessurvive(strong
prior: twoeffectiveaxes,notfive).
1.7.4 Thebiggesthiddenrisks
1. Etiologyconfound(thebigone). Pooledbaserateshidetheeffect;fadinginformation-
repricingtrendsproducessystematiclossesthatcanceltherealedge. Mostlikelycauseofa
falsenegative.
2. Systematicµ∗-lagbiasdefeatsP3. Mostlikelycauseofafalsepositive.
3. Selectionbiasinoutcome-conditionedsignaturestudies. P1-as-writtenconfirmsCSU
byconstruction.
4. Double-countingcoupledfeatures. AR(1)andvarianceareonesignal;usingbothbreaks
theindependenceassumptionbehindBonferroni.
5. Program-levelmultipletesting. Thetrueresearcherdegreesoffreedom(instruments,
frequencies,targets,document-spanningspecs)farexceedanywithin-stagecorrection.
Thelockedhold-outmustbetouchedonce.
6. Thepublic-datapriorisadverse. Thecleanestversionlikelyneedsintraday,aggressor-
classifiedflowothersdonottriviallyhave.
7. Stop-outasymmetrydominatestheP&Ldistribution. Theedgeisnotintheaverage
fade;itisinnottakingthewrong-etiologyfade.
1.8 Finaladversarialverdict
DidtheoperationalformofStateTsurvivetheredteam?
Partially—andonlyaftersurgery.
What dies: State T as currently operationalised — CSU-as-identity, five-axis gate, single-
asset daily, P1/P3 as written, pooled base rates. The flagship signature is statistically
self-confounded;thegatehasaselectionholeandasystematic-biasblindspot;thedesign
omitstheonevariable(etiology)mostlikelytobedecisive.
Whatsurvives,andwhy: theunderlyingobject—athreshold-activated,flow-carriedsign
changeintheresidual’sconditionaldrift,recognisedlatebyacrowdwhosemigrationhasa
finitetimeconstant—isreal,economicallygrounded,andnowhasabetteridentity(pressure
balance),arigorousgenerativebackbone(queuing),andareasonthegapexists(MFG).Itsurvives
asaniche,capacity-light,etiology-conditional,probably-intradayedge.
Thenarrowerversionmostlikelytolive. Intraday,onflow-driventrendsonly(etiology-
gated),fadestretchedresidualswhentheorder-flow-imbalancedrifthasflippedtowardvalue
whilepositioningisstilllight;sizebyacalibrateddiscrete-timehazard;treatCSUasatmostone
confirmatorycovariate;validateearlinessagainstaqueuingsimulatorbeforetrustingreal-data
lead–lag. Thatsentenceisthesurvivablethesis.
Theonenumberthatstilldecideseverything: theetiology-stratified,cost-clearedtradeable-
21

AdaptiveMean-ReversionProgramme FromTheoreticalObjecttoMeasurableEdge
fadebaserate,andtheleadoftheflow-imbalanceflipoverrecognition. Theorycannotmove
thesefurther. Thefrozentheoryisconverged;theoperationaltranslationisnot—andits
twolargesterrors(CSUprimacy,missingetiology)arebothfixablebeforeasingledollarof
model-building.
22

Editorial Bridge: From Critique to
Reconciliation
Theadversarialpassdiditsjob: itchangedseveralload-bearingassumptions. Thecritical-
speeding-up signature lost its status as the identity of State T; the order-flow / pressure-
balanceobjecttookitsplace;trendetiologywasexposedasamissing,decisiveconditioning
variable; and the natural model class was pinned down as a discrete-time hazard panel
ratherthananythingheavier. NoneofthisoverturnstheconvergedtheoryofStateT—butit
substantiallyrevisesitsoperationalform.
A critique that changes assumptions creates an obligation: to say plainly what now
survives,whatwasrevised,andwhatremainsgenuinelyopen. ThatistheworkofPartII.It
reconcilestheoriginalresearchmandateagainsttheframework’sactualstate—separating
whatisdecided(andshouldnotbere-litigated)fromwhatisgenuinelyunresolvedatthe
implementation level — and then explores, at depth, only the open frontier. Two things
willemergeasthetruecentreofgravity: informationrelevance(whichinformationmatters,
when,andhowitsimportanceshouldevolve)andthedatafeasibilitythatgateseveryelegant
proposal. ThefirstbecomesthesubjectofPartIII;thesecondbecomesthefirstexperiment
theprogrammemustrun.
A reader can treat Part II as the project’s corrected map: it inherits Part I’s pivots as DIRECTION
ACCEPTED,fixestheirplaceinthearchitecture,androuteseverythingintoasingleempiricalgate. If
PartIasked“cantheframeworksurvivereality,”PartIIanswers“hereistheframeworkthatdoes,and
hereistheorderinwhichtotestit.”
23

Part II
| Reconciliation | and the | Corrected |
| -------------- | ------- | --------- |
Research State
24

CHAPTER2
Research-State Reconciliation &
Open-Methodology Map
Type: Reconciliation+targetedmethodologyexploration. Not asurvey,not apaper,not areopeningof
solvedconceptualground.
Scoperule: Exploreaggressivelyonlywhereimplementationisgenuinelyunresolved. Everythingfrozen
iscited,notre-litigated,andchallengedonly whereagenuinelysuperiorimplementationpathorahidden
contradictionemerges.
2.1 Purposeandhowtoreadthis
Theprogrammehasproducedanunusualamountofconvergedtheory: aspecifiedequilib-
riumestimator(µ∗ /AnchoredKalman),aspecifieddetectionlayer(MRScore/DRC),anda
frozenregime-transitionontology(StateT,withitsred-teamcorrections). Aliteralreading
of the original mandate — a broad methodology survey across equilibrium estimation,
informationrelevance,classification,regimedetection,anddeployability—wouldre-survey
groundtheprojecthasdeliberatelyclosed.
This part does something more useful. It reconciles the mandate against the actual
state of the framework — saying plainly what is decided, what is genuinely open, and
whereexplorationaddsvalueversuswhereitwouldonlyre-litigatesettledchoices—and
thenexplores,atdepth,onlytheopenfrontier,witheveryproposalframedtosharpenthe
empiricalexistencegatethatthefrozenworkalreadyidentifiedasthetruebottleneck.
Thecentreofgravity
Thesinglehighest-leverageunresolvedproblemisnolongerequilibriumestimation
or regime ontology — both are largely settled. It is information relevance: what
informationmatters,whendoesitmatter,andhowshoulditsimportanceevolvethroughtime?
Tightly coupled is a question the frozen framework never asked: which information
mattersinwhichmarket,andwhy? Andgatingbothisaquestiontheorycannotanswer:
whatdataactuallyexists,atwhatfrequency,quality,andcost?
Theoperatingphilosophythisinheritsandkeeps: simple→interpretable→robust→useful
beforecomplex→elegant→fragile;out-of-sampleoverin-sample;economicsignificanceover
statisticalsignificance;and“stoppingisasuccessfuloutcome.”
2.2 Theframeworkasitactuallystands
Asharedstatemap,sonothingdownstreamarguesfromadifferentbaseline. Statusisoneof
FROZEN(decided;donotreopenwithoutstrongnewevidence),SPECIFIED—PRE-EMPIRICAL
(fullydesigned,awaitingdata),or OPEN(genuinelyunresolvedattheimplementationlevel).
25

AdaptiveMean-ReversionProgramme Research-StateReconciliation&Open-MethodologyMap
Object Corecommitment Status
Layer
MRScore/DRC IsthismarketfavourableforMR,anddoes SPECIFIED
L1—Detection itempiricallyrevert?3-blockscore;DRC
(forward-return-on-zregression,β < 0)is
theprimarymetricandvalidationanchor.
µ∗/Anchored LatentequilibriumtrackedbyaKalmanfil- SPECIFIED—
L3 — Equilib- Kalman teranchoredtoVWAP;anti-drifttheorem; PRE-EMPIRICAL
rium CUSUMbreakdetection;confidencescore;
DAGthatbreakstheregime↔equilibrium
circularity.
StateT(MRigni- A→T→B;T=aflow-carried,threshold- THEORY
L2 — Regime tion) activatedsign-changeinconditionalresid- FROZEN;GATE
transition ualdrift,recognisedlatebyacrowdwitha PENDING
finitetimeconstant.
Red-teampivots CSUdemotedtoweakdiagnostic;order- DIRECTION
L2(correction) flow/pressure-balancepromotedtopri- ACCEPTED
mary;trend-etiologygateidentifiedasthe
missinglayer;hazard/survivalpanel+
meta-labelisthenaturalmodelclass.
Validationdisci- Purged/embargoedCV,sample- FROZEN
Cross-cutting pline uniquenessweighting,block-bootstrap
null,pre-registerednumerickillcriteria,
lockedhold-out,multiple-testingcontrol.
Philosophy Anti-overfitting;finance-firstinterpretabil- FROZEN
Cross-cutting ity;robustnessoverelegance;implemen-
tationrealism;premature-optimisation
prohibition.
Theshapeoftheopenspace. (1)Theverticalmachinery—estimateequilibrium,measure
deviation,detectreversionregime—isessentiallybuilt. (2)Thegenuinelyunbuiltpieces
arehorizontalandconditional: howtoweightinformationasconditionschange(§2.4),how
thatweightingdiffersacrossmarkets(§2.5),andhowtocomposethegatesintoonedecision.
(3)Thewholeedificeissuspendedaboveanuntestedassumptionaboutdataaccess(§2.7),
whichthefrozendocsflag(E0)butneverresolve.
2.3 Mission-to-statereconciliation
Eachofthemandate’sfiveareas,judgedas: whatitasks→whatisalreadydecided(andwhy)→
whatisgenuinelyopen→verdict.
2.3.1 Equilibriumestimation
Already decided (do not reopen). The Anchored Kalman is Tier 1, chosen with stated
reasons over rolling mean and EMA (no uncertainty quantification; trend contamination;
ARMA(1,1)-equivalencemakesEMAasub-case),overOU-impliedequilibrium(near-unit-
rootvariance∼104×,empiricallyuselessatn = 60),andoverS/Rmidpoints(lookahead).
HMMisrejectedastheequilibriumengine(itmodelstransitionsaszero-widthjumps);particle
filteringisdeferredtothejump-augmented-OUextension.
Genuinely open. (a) adaptive-Q variants; (b) robustness under non-Gaussian inno-
vations; (c) the µ∗-construction-illusion correction — a lagging µ∗ manufactures appar-
ent reversion, a systematic bias invisible to the frozen small-perturbation test (P3), requir-
26

AdaptiveMean-ReversionProgramme Research-StateReconciliation&Open-MethodologyMap
inganacausal/structurally-differentbenchmarkinstead;(d)thedeeperchallengethatin
information-repricingtrendstheequilibriumitselfmoved—sothequestionisless“estimateµ∗
better”than“knowwhenµ∗ isthewrongobject.”
Equilibriumestimationisclosed;re-surveyingfiltersaddsnothing. Only(a)–(d)merit
attention,andtheyarevalidation/conditioningquestions,notestimator-choiceques-
tions.
2.3.2 Information-relevancearchitecture
Already decided: very little. The weighting system is marked “still under ideation”;
MRScore uses fixed economic-prior block weights (20/60/20) precisely to avoid in-sample
weightoptimisation—adeliberatenon-answerthatresistsoverfittingbutdoesnotadapt.
Genuinelyopen: essentiallythewholeproblem.
Thisisthehighest-leverageopenproblem. Itisthecenterpiece(§2.4),anditsfull
mathematicalformalizationisPartIII.
2.3.3 MR-opportunityclassification
Theconceptualclassificationexistsinasharperformthanthemandate’sA/B/C:StateT’s
A→T→Balreadyencodes“continuation(don’tfade)→earlytradeablereversion→crowded
reversion(edgegone),”andCUSUM+thevaliditygatehandlethestructural-breakcase.
Themethodisalsochosen: adiscrete-timehazard/survivalpanel+meta-label. Genuinely
open: theintegrationwiring—howthe µ∗ validitygate,theStateThazard,andthe(new)
etiologygatecomposeintoonedecision.
2.3.4 Regimedetection&structuralbreaks
Alreadydecided: equilibrium-levelbreakdetection=CUSUMonnormalisedinnovations;
MR-favourability regime = RFI (variance-ratio + ADF) and MRScore; “when to distrust
µ∗”ispartlyansweredbythevaliditygateV andKalmanStab. Genuinelyopen: thetrend-
t
etiologyclassifier—thered-team’ssinglemostconsequentialomission,afast,conditional,
episode-levelregimevariableorthogonaltoMRScore.
2.3.5 Real-worlddeployability
Alreadydecidedasprinciples: thepremature-optimisationprohibition,killcriteria,interpretability-
first,thehazard-not-deep-learningchoice. Genuinelyopen: thebindingdeployabilityques-
tionsareempiricalandunanswered—whatdataexists,atwhatfrequency,quality,and
cost(E0),thedaily-vs-intradaydecision,capacity/crowding-fragility,andtheadverseprior
thatthepublic-datadailyedgeispartiallypre-arbitraged.
2.3.6 Thereconciliationinonematrix
27

AdaptiveMean-ReversionProgramme Research-StateReconciliation&Open-MethodologyMap
|     | Decided(don’treopen) | Genuinelyopen | Where |
| --- | -------------------- | ------------- | ----- |
Mandatearea
|     | AnchoredKalman;alterna- | adaptive-Q,robustness,µ∗- | §2.6 |
| --- | ----------------------- | ------------------------- | ---- |
illusioncorrection,“isµ∗the
| Equilibrium | estima- tivesrejectedwithreasons |                      |         |
| ----------- | -------------------------------- | -------------------- | ------- |
| tion        |                                  | rightobject”         |         |
|             | almostnothing(fixedpriors        | thewholearchitecture | §2.4;   |
| Information | rele- only)                      |                      | PartIII |
vance
|     | A→T→B;hazard+meta- | integrationwiring;“TypeC”↔ |     |
| --- | ------------------ | -------------------------- | --- |
§2.6
| MRclassification   | labelmethod        | info-repricing           |           |
| ------------------ | ------------------ | ------------------------ | --------- |
|                    | CUSUM;RFI;MRScore; | trend-etiologyclassifier | §2.5,§2.6 |
| Regime/breakdetec- | validitygate       |                          |           |
tion
|     | principles(anti-overfit, | datafeasibility,frequency,ca- | §2.7 |
| --- | ------------------------ | ----------------------------- | ---- |
Deployability
|     | interpretability) | pacity |     |
| --- | ----------------- | ------ | --- |
2.4 Information-relevancearchitecture(thecenterpiece)
Thequestion
Whatinformationmatters,whendoesitmatter,andhowshoulditsimportanceevolvethrough
time?
Everything else — equilibrium, detection, even the State T hazard — is a machine for
processinginformationwhoserelevanceisassumed. Thissectionaskshowrelevanceitself
shouldbemeasured,weighted,andupdated,underaharddisciplineborrowedfromthe
CommodityForecastingpaper(Ahmed&Tsvetanov2016),usednotasforecastingbutasa
cautionarycontrol.
| 2.4.1 Thediscipline: | fivelessons |     |     |
| -------------------- | ----------- | --- | --- |
Statisticalsignificance̸=economicsignificance.
| 1.  |     | Relevancemustbescoredbyout-of- |     |
| --- | --- | ------------------------------ | --- |
sampleeconomicvalue,neverbyin-samplet-statistics.
2. Out-of-sample > in-sample. Every relevance estimate is itself an OOS quantity; in-
samplefeatureimportanceisinadmissible.
3. Conditionalvs.unconditional—andthetrap. Thepaper’sactualfindingisthatuncondi-
tionalfactorexpectationsforecastbetterOOSthanconditionalones,becauseconditioning
adds estimated parameters and the estimation noise overwhelmed the signal. Condi-
tioningisnotfree. Anyregime-conditionedweightingmustbeatitsownunconditional
baselineOOS,oritisrejected.
4. Structural instability matters. Relevance drifts — but lesson 3 says time-varying rel-
evance must be done parsimoniously, or instability-tracking degenerates into noise-
tracking.
5. Sophisticated models routinely fail to beat simple baselines. The benchmark every
scheme must clear is a simple, fixed-weight baseline; complexity that does not beat it
OOSisdeleted.
28

AdaptiveMean-ReversionProgramme Research-StateReconciliation&Open-MethodologyMap
These five compress to one operating rule: disciplined information relevance, not
predictive complexity. Each method below is judged through four points — core
assumption,problemsolved,failuremodes,deploymentfit—andthenagainstthese
fivelessons.
2.4.2 Methodsevaluated
Problemitsolves/failuremode Verdict
Method
relevancedrift;butaderivative-of-a-noisy- Demotetodiagnostic
Rolling explanatory statistic,in-sampleinsideeachwindow
power
featureexplosion,overfitting,noise;static(no Adoptasstaticback-
Shrinkage/elastic-net regimeadaptation) bone,penaltyfixed
fromtheory
regimedependence,heterogeneity;butlesson3 Adopt,coarse(≤ 3),
Regime / etiology- bites—splintersthesample withpartialpooling
conditionedweights
drift+regimejointly;butevent-starvedat Defer(denserdata)
Bayesianupdating/DMA daily,λoverfit-prone
model-freenonlinearscreening;sample-hungry, Offlineaxis-selection
Entropy/mutualinforma- nodirection only
tion
signalinstability,falsepositives;asecondplace Keep,low-capacity
Meta-model / meta- tooverfit formonly
labelling
everythinginprinciple;disqualifyingdata Reject
Reinforcement / online starvation
learning
deepesttransportability;infeasibleidentifica- Parkasnorthstar
Causalrelevance tioninmarkets
2.4.3 Therecommendedarchitecture
Thearchitecture’sspineinoneline
Screenoffline → shrinktowardaneconomicprior → conditiononlycoarselyandonlywith
partialpooling→trustviaalow-capacitymeta-label→andletnothingsurvivethatcannot
beatasimplebaselineonout-of-sampleeconomicvalue.
Concretely: (1) a small, pre-registered axis set (≤ 5, realistically ≈2 effective: a price-
residual axis and a flow/positioning axis), screened offline by MI / economic reasoning;
(2)astaticbackboneofelastic-netshrinkagetowardaneconomicprior,penaltyfixedfrom
theory;(3)coarseregime/etiologyconditioningwithpartialpooling—abucketonly“earns”
its own weights by beating pooled OOS economic value; (4) a low-capacity meta-label /
hazardasthetrustlayerandsourceofcalibratedsizingprobabilities;(5)thenon-negotiable
protocolthateverylayermustbeatasimplefixed-weightbaselineonOOScostedeconomic
value,underpurgedCVandablock-bootstrapnull;(6)DMA/Bayesianforgetting-factor
weightingdeferredtoadenser-datafuture. PartIIIturnsthisarchitectureintoafullyspecified
29

AdaptiveMean-ReversionProgramme Research-StateReconciliation&Open-MethodologyMap
mathematicalengine.
2.5 Market-adaptiveinformationarchitecture
Thequestion§3cannotansweralone
Whichinformationmattersinwhichmarket,andwhy?
The information that ignites a tradeable State T in an index future is not the information
that does so in a commodity spread. State T’s mechanism (flow exhaustion / inventory
completion) only exists in markets whose trends are flow-driven and exhaustible — not in
marketswhosetrendsareinformationrepricing. Relevanceisthereforenotapropertyofthe
instrumentbutofthe(instrument×currentetiology)pair.
2.5.1 Markettaxonomy
|               | Dominanttrendetiolo- | TradeableT | Informationthatlikelymatters |
| ------------- | -------------------- | ---------- | ---------------------------- |
| Marketclass   | gies                 |            |                              |
|               | dealer/gammaflow;    | HIGH       | OI&OI-change;options         |
| Index futures |                      |            |                              |
|               | CTA&systematic       |            | skew/gamma;breadth;volterm   |
| (NIFTY,ES)    | flow;positioning     |            | structure;basis              |
crowding;macroon
eventdays
|                   | inventorycycles;sup- | MIXED | inventories(EIA/USDA);curve;sea- |
| ----------------- | -------------------- | ----- | -------------------------------- |
| Commodity         | plyshocks;seasonal-  |       | sonality;COT;rollyield           |
| futures(outright) | ity;carry/roll       |       |                                  |
|                   | relativestorage/con- | HIGH  | curveshape;storage;seasonalde-   |
Commodity
|               | venienceyield;cointe- |     | mand;processingmargins |
| ------------- | --------------------- | --- | ---------------------- |
| spreads (cal- | gratedlegs            |     |                        |
| endar, crack, |                       |     |                        |
crush)
|     | ratedifferentials; | LOW–MOD | ratedifferentials;CBcalendars;CFTC |
| --- | ------------------ | ------- | ---------------------------------- |
FXfutures
|     | macro/CBrepric- |     | positioning;carry |
| --- | --------------- | --- | ----------------- |
ing;positioning
|     | policyrepricing;auc- | LOWat | auction&macrocalendar;curve; |
| --- | -------------------- | ----- | ---------------------------- |
Ratesfutures tionsupply;macro events positioning;CBcommunication
data
|     | idiosyncraticdecou- | HIGH | cohortco-movement;residualdecou- |
| --- | ------------------- | ---- | -------------------------------- |
Relative-value / plingwithinaco- (capacity- pling;cointegration;relativeposition-
| cross-sectional | movingcohort | robust) | ing |
| --------------- | ------------ | ------- | --- |
Readingthetaxonomy. Thecrowdingaxisisonlyasgoodasitsdata: cleanlyobservable
inindexfutures(OI+EODoptions),reasonableincommodities(OI+weeklyCOT),but
weak and lagged in FX/rates — which alone argues index futures first. FX and rates are
thenaturalskeptic’smarkets: theirdominantetiologyisinformationrepricing,sotheyare
excellentnegativecontrolsbutpoorfirsthomes. Spreadsandcross-sectionarethestructurally-
favourablefrontier—equilibriumanchoredbyeconomicsratherthanafragilestatistical
estimate—andthecross-sectionalformgivesaκ-freeearlinessproxy.
30

AdaptiveMean-ReversionProgramme Research-StateReconciliation&Open-MethodologyMap
2.5.2 Universalcorevs.market-specificmodules
Thearchitecturalverdict: auniversalcoreplusthinmarket-specificmodules—not
onefixedsignalstack,andnotaseparatemodelpermarket.
Theuniversalcore(identicalacrossmarkets)istheresidualconstructionε = P−µ∗,the
standardised deviation z and entry filter, the concept of a crowding/recognition axis, the
costedtriple-barrier(C3)label,theetiology-gateslot,thediscrete-timehazard+meta-label,
andtheentirevalidationdiscipline. Themarket-specificmodules(swappedpermarket)
aretheetiologyclassifier’sinputs,thecrowdingproxy,thecostmodel(roll/carrymatters
forcommoditiesandFX),andmarket-specificseasonality/curvefeatures. Everymodule
isafreshsetofresearcherdegreesoffreedom,soeachmustindependentlyclearthesame
OOSeconomic-valuebaragainstthecore-with-no-modulebaseline. Sequencing: buildthe
universalcoreplusonemoduleonthemostfavourable,mostdata-accessiblemarket—index
futures — prove it beats baseline OOS, and only then port the core and author a second
module.
2.6 Theremainingopenimplementationfrontier
2.6.1 Thetrend-etiologyclassifier(method)
Coarse and rule-based first, not a learned model. A defensible v0 is a 3-way label —
{flow/behavioural, information-repricing, ambiguous}—fromcheapobservableproxies.
The information-repricing flag: a scheduled macro/policy/earnings event in the window
and/oragap-and-vol-jumpsignature(overnightgap> kσwitharealised-volregimeshift)
—“theequilibriummayhavemoved;donotfade.” Theflow/behaviouralflag: atrendaccom-
paniedbyOIbuildthatsubsequentlystalls,absentascheduledevent—“exhaustibleflow;
fadeable.” Ambiguous: tradesmallerorstandaside. Thedecisiveuseisstratification: every
base-rateandpredictabilitystatisticmustbecomputedwithinetiologybuckets.
2.6.2 Flow/pressure-balanceoperationalisation
The implementation question is the live-vs-offline split, governed entirely by data. Live
(if data exists): a reduced-form signed OFI and its short-horizon drift sign (price change
≈OFI/depth). Offlineonly: thequeuingmodelasasynthetic-ground-truthsimulatorand
thesourceofthehazard’sfunctionalform;themean-fieldgameastheexplanationofwhya
recognitiongapexistsandadisciplinefordefiningcrowdingasmass/migration. Ifaccessible
data cannot deliver a usable OFI proxy at the right frequency, the flow-as-primary-identity must
degradegracefullybacktowardthecrowdingaxisandpartial-reversionstatistics.
2.6.3 Equilibrium-layeropenitems
Estimationisclosed. Thethreeliveitems: adaptive-Q(deferreduntilthefixed-Qbasemodel
isvalidated);non-Gaussianrobustness(deferred,activateonlyondemonstratedJB-rejection
+highCUSUMfalse-positiveevidence);andtheµ∗-construction-illusioncorrection(areal
fix)—replaceP3withacomparisonagainststructurally-differentandacausalbenchmarks
(afuture-awaresmoothedequilibriumand≥ 2estimatorsofgenuinelydifferentfamily). If
thereversionsignaturesurvivesonlyagainstthefrozencausalµ∗ butvanishesagainstan
acausalequilibrium,itwasµ∗ catch-up,notreal.
31

AdaptiveMean-ReversionProgramme Research-StateReconciliation&Open-MethodologyMap
2.6.4 Classification&integrationwiring
Theproposeddecisionpipelineisaconjunctivegate,orderedcheapest-and-most-decisive
first:
Question
# Gate
Isthisafadeabletrendtype? Information-repricing→
1 Etiologygate standaside. (Cheapest,mostdecisive.)
Is µ∗ valid (V = 1, KalmanStab) and |z| ≥ z with
t entry
2 Deviation + signopposedtotrend?
equilibrium-validity
Isrecognitionstilllight(OI-changevs.range;position-
3 Crowdinggate ing)? Isitearly?
Thecalibratedprobabilitysetssize;theC3costedlabel
4 Hazard / meta-label trainsandscoresit.
sizing
Opendesignchoices—hard(strictAND)vs.soft(aprobabilisticproductfeedingthehazard)
gates,orderingunderdataconstraints,andhowthemandate’s“TypeCstructuralbreak”
mapsin(answer: theetiologygate’sinformation-repricingbranchplustheCUSUMbreak
flag)—areresolvedempirically.
2.6.5 Cross-sectionalformulation
Fadinganame’sresidualonceithasdecoupledfromitsco-movingcohortwhilethecohort
stilltrendsgivesthreeadvantages: aκ-freeearlinessproxy,capacityrobustness,andpartial
etiology-hedging. Verdict: the strongest second formulation after the single-asset index-
futurescoreisproven;alsothedataregimewhereDMAbecomesviable. Flag,donotbuild
first.
2.7 Datafeasibilityandoperationalconstraints
Therealityfilter
Inaccessiblesignal=nonexistentsignal. Methodologymustbegatedbywhatdataactually
exists — at what frequency, quality, and cost — assuming no institutional-quality
proprietaryfeeds.
Thissectionisfirst-classbecauseitdecideswhichoftheabovesurvives. Severalelegantproposals
(flow-as-primary-identity,intradayOFI)liveordiehere.
32

AdaptiveMean-ReversionProgramme Research-StateReconciliation&Open-MethodologyMap
|      |     | Accessible | Frequency | Verdictforthisprogramme |
| ---- | --- | ---------- | --------- | ----------------------- |
| Data |     | (non-      |           |                         |
proprietary)?
✓foundational
|                       |     | Yes          | daily/   |                           |
| --------------------- | --- | ------------ | -------- | ------------------------- |
| OHLCV+volume          |     |              | intraday |                           |
|                       |     | Yes(exchange | daily    | ✓centraltothecrowdingaxis |
| Openinterest(futures) |     | EOD)         |          |                           |
|                       |     | Yes(vendor)  | intraday | ✓neededif dailyaliases    |
Intradaybars(1m–1h)
|     |     | Largelyno |     | △thebindingconstraint(quasi- |
| --- | --- | --------- | --- | ---------------------------- |
sub-
| OFI / aggressor-side |     |     | sec–min | proprietary) |
| -------------------- | --- | --- | ------- | ------------ |
flow
✓strengthensindex-first
|                     |     | Yes(EOD | daily |     |
| ------------------- | --- | ------- | ----- | --- |
| Options positioning | /   | chains) |       |     |
skew/gamma(index)
|                     |     | Yes(CFTC) | weekly,   | △slowcontextonly |
| ------------------- | --- | --------- | --------- | ---------------- |
| COTpositioning(com- |     |           | ∼3-daylag |                  |
modities/FX)
weekly/month✓lyetiologyinput
Yes(EIA,
| Inventory | reports | USDA) |     |     |
| --------- | ------- | ----- | --- | --- |
(commodities)
✓cheap,high-ROIetiologyinput
|               |        | Yes | as-       |     |
| ------------- | ------ | --- | --------- | --- |
| Macro / event | calen- |     | scheduled |     |
dars
|                     |     | Yes(futures | daily | ✓commodity/ratesmoduleinput |
| ------------------- | --- | ----------- | ----- | --------------------------- |
| Curve/termstructure |     | chain)      |       |                             |
Whatthedatarealitydoestothemethodology. Theflow-as-primary-identityisthemost
data-fragile proposal: a clean live OFI requires message-level or tick data with aggressor
classification,effectivelyproprietary-grade. AtdailyfrequencytheOFIidentitycannotbe
implemented faithfully; only lossy proxies exist, and if they are too lossy, the crowding
axis(OI/options,whichisaccessible)mustcarrytheidentityinstead—amaterial,honest
downgraderisk. Thecheapestdata(calendars,OI,EODoptionchains,curve)isthehighest-
ROI:thedataeconomicsindependentlyfavourthesamefirstmarket(indexfutures)andthe
sametwodecisiveaxesasthetheory. COTistooslowtobealivecrowdingaxis. Intradayis
acostdecision,notacapabilitygap.
Thesurvivalrule. Amethodologysurvivesonlyifitsinputsareaccessible,timely,and
affordablewithoutproprietaryfeeds—oriftheprogrammeexplicitlypaysforthedata
andthecostisjustifiedbyOOSeconomicvalue. Bythisrulethecrowdingaxis, the
etiologygate,theµ∗
stack,andthecostedlabelallsurvivecheaply;theliveOFIidentity
isonprobationpendingE0;andanythingrequiringreal-timedealerinventoryisout.
2.8 Routingtheexplorationintotheempiricalgate
Theopenexplorationdoesnotreplacethefrozengate;itsharpensandre-ordersitandsupplies
thepre-registrationcontent.
33

AdaptiveMean-ReversionProgramme Research-StateReconciliation&Open-MethodologyMap
|     | Whatittests | Sharpenedby |
| --- | ----------- | ----------- |
Gatestep
|                  | CanyougetcleanOI/options+  | §2.7—decidesfrequencyandwhetherthe |
| ---------------- | -------------------------- | ---------------------------------- |
| E0—Datafeasi-    | ausableflowproxy+calendar, | flowidentityisreachable            |
| bility (promoted | atthechosenfrequency?      |                                    |
tofirst)
|                 | Isthecost-clearedtradeable-fade | §2.5,§2.6—stratify,neverpool |
| --------------- | ------------------------------- | ---------------------------- |
| E1 — Etiology-  | baserateabovethefloorwithin     |                              |
| stratified base | therightbucket?                 |                              |
rate
|               | Istheeventseriesnon-IID(a | Unchanged;almostfree                  |
| ------------- | ------------------------- | ------------------------------------- |
| E2—Clustering | regimetodetect)?          |                                       |
|               | Onqueuing-simulatedflow   | §2.6—estimatorworksbeforetrustingreal |
E3 — Synthetic
|                | withaknownfliptime,does      | data |
| -------------- | ---------------------------- | ---- |
| earliness(new) | thedetectorfinditbeforeprice |      |
reversion?
|                | DoestheproxyOFI-driftsign    | lead–lagofprobabilityseries,notwindow  |
| -------------- | ---------------------------- | -------------------------------------- |
| E4 — Real flow |                              |                                        |
|                | changeleadOI/positioning     | width;replacesCSU-basedP2              |
| lead–lag       | build-up?                    |                                        |
|                | Isthereversiontowardacon-    | acausalbenchmark,notsmallperturbation; |
| E5—Acausal-µ∗  | temporaneousequilibrium,orµ∗ | replacesP3                             |
test
catch-up?
|               | Doesthecrowdingaxisseparate | Unchanged;thedecisiveClaim-Ptest |
| ------------- | --------------------------- | -------------------------------- |
| K4 — Crowding | earlyfromcrowdedfades?      |                                  |
separation
theetiologyclassifierandits3buckets;the≤ 5(≈
Pre-registeredbeforetouchingdata: 2
effective)axesandthesinglestatisticperaxis;theOOS-economic-valueevaluationprotocol
andthesimplefixed-weightbaselineeveryrelevancelayermustbeat;theinstrument/fre-
quency/ target set (bounding the garden of forking paths); and the numeric kill criteria
K1–K5.
2.9 Recommendationsandrankedroadmap
2.9.1 Immediatepriorities(highestROIfirst)
1. E0 data feasibility on one index future (NIFTY or ES). Confirm cheap access to EOD
OHLCV+OI,EODoptionchains,andamacro/eventcalendar;assessflowproxies;price
intradaytickdata. Thissinglestepdecidesfrequencyandwhethertheflowidentityisreachable.
2. Locktheinformation-relevanceevaluationprotocol: thesimplefixed-weightbaseline,
theOOS-costed-economic-valuemetric,purgedCV,theblock-bootstrapnull.
Buildthecoarserule-basedetiologygatefromcheapdata(calendar+gap/vol-jump+
3.
OI-build-then-stall).
4. Runtheetiology-stratifiedbase-rateandclusteringstudy(E1/E2)ontheindexfuture.
2.9.2 Whatisdeferred,andwhatshouldstopbeingresearched
Deferred(rightidea,wrongtime): adaptive-Qandnon-Gaussian/particleextensions;DMA
/Bayesianforgetting-factorweighting(untilintradayorcross-sectionaldensityexists);the
cross-sectional formulation; MFG and full queuing in the live stack (offline only); the 5-
axisdetector(startwith≈2);multi-timeframe;allsignal/sizing/exitoptimisation.
Should
34

AdaptiveMean-ReversionProgramme Research-StateReconciliation&Open-MethodologyMap
stop being researched: CSU-as-identity; any in-sample or purely statistical-significance
validation;broadequilibrium-estimatorsurveys;derivatives-of-noisy-statistics;anysign-
blind / symmetric architecture; RL and deep sequence models at this data regime; and
treatingAR(1)-of-εanddeviation-varianceastwosignals(theyareone).
2.9.3 Ifcodingstartedtomorrow: exactlywhatv0contains
Adeliberatelyminimal,interpretable,single-marketsystemononeindexfuture,daily
(intradayheldinreserve):
▶ Data: EOD OHLCV + OI; EOD option chain (skew/positioning); macro/event
calendar;basis.
▶ Equilibrium: AnchoredKalmanµ∗ (frozen)→residualε →standardisedz.
▶ Gate1—Etiology: rule-based3-way;standasideoninfo-repricing.
▶ Gate2—Deviation: |z| ≥ z ,signopposedtotrend,µ∗ valid.
entry
▶ Gate3—Crowding: OI-change-vs-range(+option-positioningskew).
▶ Label: C3costedtriple-barrier(σRV barriers,fixed H).
▶ Model: low-capacitydiscrete-timehazard(pooledlogistic);calibratedprobability
setssize.
▶ Relevance: ≈2axes,elastic-netshrinkagetowardaneconomicprior;coarseetiology
conditioningwithpartialpooling.
▶ Harness: purged/embargoedCV,block-bootstrapnull,sample-uniquenessweight-
ing, locked hold-out, pre-registered kill criteria, simple-baseline OOS-economic-
valuebenchmark.
▶ NOT in v0: CSU axis; κ-complex/timescale/nonlinear-activation axes; live OFI;
DMA/RL;multi-timeframe; cross-sectional; sizing/exitoptimisationbeyondthe
hazardprobability.
Thesinglehighest-leveragenextmove. RunE0—datafeasibilityononeindexfuture
—jointlywithlockingtheinformation-relevanceevaluationprotocol(OOSeconomic
value vs. a simple baseline). Resolve those two facts, in days, and the rest of the
roadmapbecomesexecutableoriscleanlykilled. Donotbuildthesignalfirst. Establish
thedataandthemeasuringstick,thenrunthecorrectedgate.
35

Editorial Bridge: From Architecture to
Mathematics
Part II isolated a single problem as the highest-leverage unsolved piece of the entire pro-
gramme: information relevance. It also gave that problem an architecture — screen offline,
shrinktowardaneconomicprior,conditioncoarselywithpartialpooling,trustviaalow-
capacitymeta-label,andletnothingsurvivethatcannotbeatasimplebaselineout-of-sample.
Butanarchitectureisnotyetaspecification. Thewords“relevance,”“confidence,”and“mat-
ters”wereusedrepeatedlywithoutamathematicaldefinitionthatsoftwarecouldevaluate.
PartIIIclosesthatgap. Itdefines,precisely,whatitmeansforapieceofinformationto
matterinaregime;itseparatesthatfromhowmuchweshouldtrustthemeasurement;andit
fusesthetwointoasingleweightthesystemactson. TheresultistheConditionalRelevance
Engine(CRE)—adeliberatelysmall,interpretable,out-of-sample,adaptiveestimatorthat
dischargeseveryrequirementPartIIraised. Crucially,theCREisnotasixthlayerbolted
onto the side. It is the connective tissue: once relevance is a number, “which DRC input
mattersnow,”“whichequilibriumestimatorismostusefulnow,”and“whichsignalisfiring
beforethecrowd”allbecomethesamemathematicalquestion.
Thisistheculminationofthedossier. PartIchallengedthetheory;PartIIcorrectedthearchitecture;
PartIIIformalisesthemathematicsand,withit,declarestheframeworkimplementation-ready—starting,
aseveryhonestplaninthisprogrammedoes,withthedataandthelabelratherthanthesignal.
36

|             |              | Part        | III           |            |
| ----------- | ------------ | ----------- | ------------- | ---------- |
| Conditional |              | Information |               | Relevance: |
| The         | Mathematical |             | Formalization |            |
37

CHAPTER3
The Conditional Relevance Engine
Researchphase: Workingpaper,convergingtowardimplementationspecification.
Audience: Financeprofessionalsfirst,quantssecond. Mathematicssupportsthenarrative;itdoesnot
dominateit.
3.1 Executivesummary
Theprojecthasreacheditslastconceptualbottleneckbeforesoftwarecanbebuilt: wedonot
yethavearigorous,agreeddefinitionofwhichinformationmatters,whenitmatters,and
howconfidentweareinthatjudgment. Everylaterlayer—regime-shiftdetection,equilib-
rium estimation, signal generation — silently assumes this question is already answered.
Itisnot. Thispart(1)defineswhat“mattering”and“confidence”meanmathematically,(2)
evaluatesthecandidatetoolshonestlyagainsttheprojectfilters,and(3)commitstoasingle
minimalframeworkthatcanbeimplementednow.
Thecommittedanswer,inoneparagraph
Relevanceistask-anchored,regime-conditional,incremental,out-of-samplepredic-
tivecontributionthatpersiststhroughtime. Apieceofinformationmattersinaregime
if,giveneverythingwealreadyknow,addingitmeasurablyimprovesourabilityto
predictthespecificmean-reversionoutcomewetrade—andifthatimprovementis
stable,notaone-shotartifact. Confidenceisaseparatequantity: itmeasureshowmuch
we trust the relevance estimate itself, driven by how much regime-specific data we
have,howstabletheestimateisacrossresampling,andwhetherin-samplerelevance
survivesout-of-sample. Wecarryrelevanceandconfidenceastwodistinctnumbers,and
thesystemactsontheirproduct.
Formally,foreachinformationsourceiattimetwemaintain
R = regime-conditional,exponentially-weightedincrementalskillofsourcei, (3.1)
i,t
C = trustin R = precision×stability×regimesufficiency×OOSpersistence. (3.2)
i,t i,t
andthesystemneveruses R raw. Itusesaconfidence-shrunkeffectiveweight
i,t
w = R ·g(C ), g(C) ∈ [0,1], (3.3)
i,t i,t i,t
whichcollapsestowardzerowheneverwedonotyettrustwhatwearemeasuring. Thisis
the entire system in miniature. The workhorse estimator is deliberately simple — regime-
conditional,exponentially-weightedincrementalpredictiveskill,gatedbystabilityselection,shrunk
by confidence. Information theory (conditional mutual information / transfer entropy) is
retainedonlyasanoptionalmodel-freecross-check;deeplearning,black-boximportance,and
exoticmachineryareexplicitlyexcluded.
38

AdaptiveMean-ReversionProgramme TheConditionalRelevanceEngine
3.2 Framingthebottleneck
3.2.1 Whythisisthehardpart
Everylayerabovethisoneisconditionalonananswerto“whichinformationiscurrently
relevant.” MRScore / DRC trusts inputs that must themselves be relevant in the current
environment. Regime-shiftdetectionisliterallyastatementaboutinformation—itclaims
thatcertainsignalsbehaveabnormallybeforeanewregimeemerges,aclaimthatisempty
untilwecansaywhat“thissignalcarriedinformationaboutthecomingtransition”means
mathematically. Equilibriumestimationmustchooseamongcandidateestimators—“which
ismostusefulrightnow”isarelevancequestionindisguise. Andsignalgenerationweights
inputs—weightingisrelevancescoring. Conditionalinformationrelevanceisthereforenot
onemoremodule;itistheconnectivetissue.
3.2.2 Whatthisisnot
Notforecasting—wearenotbuildingareturnpredictor,butameta-layerthatdecideswhich
inputsaseparatedecisionprocessshouldlistento. Notgenericfeatureselection—classical
feature selection asks “which features predict Y over the whole sample”; we ask “which
featurespredictthespecificMRoutcomewetrade,inthisregime,rightnow,incrementally,and
reliably.” NotanMLalphasearch—weareformalisingajudgmentahumanquantcurrently
makesimplicitlyandinconsistently.
3.2.3 Theobjectwearetryingtobuild
Afunctionthesoftwarecanevaluateateverytimestamp:
(cid:8) (cid:9)N
(market, regimes , infosetI ) (cid:55)−→ (R ,C ) , (3.4)
t t i,t i,t i=1
returning, for each candidate information source i, a relevance and a confidence. The
deliverableofthisphaseistheprecisemathematicaldefinitionof RandCandacomputable
estimatorforeachthatsurvivescontactwithmarkets.
3.3 Whatdoes“mattering”mean? Definitionalwork
Thisisthepartmostquantprojectsskip,anditiswhytheir“featureimportance”numbers
areuninterpretable. Wedefinethetargetbeforewemeasureanything.
3.3.1 Sixcandidatedefinitions
Weconsideredsixnotionsof“thisinformationmattered.” Eachisdefensible;theyarenot
equivalent, and conflating them is the classic error. (a) Predictive usefulness for the MR
transition—directlytiedtowhatwetrade,butrequiresawell-definedtarget. (b)Explana-
torycontribution(high R2 share)—butin-sample R2 rewardsoverfitting;explanatory̸=
tradeable. (c)Incrementalinformationgain—mattersbeyondwhatwealreadyknow; kills
double-countingofredundantsignals. Essential;wekeepit. (d)Regime-conditionaluseful-
ness—mattersinaregime,notglobally;thewholethesis. Keptasaconditioningvariable. (e)
Causalusefulness—genuinecausalidentificationinmarketsislargelyinfeasible; down-
rankedtoaweakpredictive-causalitycross-check. (f)Persistence/stability—usefulnessis
notaone-shotartifact;thedifferencebetweenalphaanddata-snooping. Kept,asarequirement
ontopof(a)+(c).
39

AdaptiveMean-ReversionProgramme TheConditionalRelevanceEngine
3.3.2 Thecommitteddefinition
Committeddefinitionofrelevance
Asourceimattersinregimesattimetif,conditionalonthecurrentregimeandthein-
formationalreadyinuse,addingiproducesameasurable,out-of-sampleimprovement
inpredictingthespecificmean-reversionoutcomewetrade—andthatimprovement
persistsacrosstimeandresampling.
Four design commitments follow, each a deliberate guardrail. (1) Task anchoring —
relevance is always relative to a defined target Y. Following meta-labelling, the natural
t
targetisamean-reversionoutcomelabel: afteradeviationfromµ∗ beyondathreshold,didprice
reverttowardµ∗ byatleastκ withinhorizonh? (2)Incrementality—relevanceismeasured
againsttheexistinginformationset,neverinisolation;aconditional,notmarginal,quantity.
(3)Conditioning—everythingiscomputedgiventhecurrentregimestates . (4)Persistence
t
—arelevancespikeinasinglewindowisnoiseuntilprovenotherwise;persistenceenters
twice,insidetheestimator(exponentialweighting)andinsideconfidence(stabilityacross
resamples).
3.3.3 Themathematicalformofrelevance
LetY betheMR-outcomelabel,B thebaseinformationsetalreadyinuse(e.g.thedeviation
t t
ε = P −µ∗ andwhateverthesystemalreadytrusts),and x thecandidatesource. Let s
t t t i,t t
denotetheregime. Definetheregime-conditionalincrementalskill:
∆ = L (cid:0) Y | B; s (cid:1) − L (cid:0) Y | B,x ; s (cid:1) , (3.5)
i,t t i t
whereLisanout-of-samplepredictiveloss(log-lossforbinarylabels,ornegativepseudo-
R2). ∆ > 0meansadding x reducesout-of-samplelossinthisregime—itcarriesinforma-
i,t i
tionwedidnotalreadyhave. Thisistheatomofrelevance;the“out-of-sample”qualifieris
whatenforceshonesty.
Wethenconvertthenoisyper-window ∆ intoasmooth,adaptiverelevancebyexpo-
i,t
nentialweightingwithaforgettingfactorλ ∈ (0,1):
R = (1−λ)∆˜ + λR (3.6)
i,t i,t i,t−1
where
∆˜
is
∆
standardizedwithinregime(sodifferentmarkets/regimesarecomparable).
i,t i,t
Theforgettingfactoristhemathematicalembodimentof“informationstopsmattering”: old
evidence decays, recent evidence dominates, and λ is tied to regime stability (§3.7). This
recursionisintentionallythesameshapeastheDMAupdateandtheKalmanupdatealready
intheproject,soitcomposescleanlywiththerestofthestack.
3.4 Whatdoes“confidence”mean?
Thesinglemostimportantconceptualmoveinthispartistheinsistencethatrelevanceand
confidencearedifferentquantities. Asignalcanhavehighestimatedrelevancewebarely
trust(computedfrom12observationsinathree-day-oldregime),andmodest,rock-solid
relevance we trust completely. The software must never confuse the two, because they
implyoppositeactions: highrelevance/lowconfidencemeanswatch,donotyetsize;modest
relevance/highconfidencemeansact.
40

AdaptiveMean-ReversionProgramme TheConditionalRelevanceEngine
3.4.1 Thefourdriversofconfidence
C isnothowstrongthesignalis;itishowmuchwetrustourestimate R . Itanswers: if
i,t i,t
were-ranhistoryslightlydifferently,orwaitedformoredata,would R hold? Wedecomposeit
i,t
intofourinterpretable,separately-computablecomponents:
1. Posterior / statistical precision τ . How tight is the estimate given noise and sample
i,t
size—theinversevarianceof ∆ . Fewornoisyobservations⇒wideposterior⇒low
i,t
confidence.
2. Stability/recurrenceπ . Doestherelevancesurviveresampling? Usingstabilityselection
i,t
(Meinshausen–Bühlmann),subsampletheregime’sdatarepeatedlyandrecordtheselec-
tionprobability π = fractionofsubsamplesinwhich x isretainedasincrementally
i,t i
useful. Alsogivesfinite-samplecontroloverexpectedfalsediscoveries.
3. Regimesamplesufficiency ϕ(n ). Howmuchdataweactuallyhaveinthisregime. A
st
youngregime(smallrun-lengthfromthechangepointdetector)meanssmalleffective
sample,soconfidencemustbelowevenif thepointestimatelooksstrong.
4. Out-of-samplepersistenceρ . Doesin-samplerelevancesurviveOOS?Apersistence
i,t
ratio=(OOSskill)/(ISskill),clippedto[0,1]. TheLópezdePradodisciplinemadeinto
anumber.
3.4.2 Themathematicalformofconfidence
Becauseconfidenceshouldbedestroyedbyanysinglefailure(apreciseestimatethatdoesn’t
replicateisstilluntrustworthy),weuseamultiplicativeformratherthananaverage:
C = σ(β +β τ ) × π × ϕ(n ) × ρ (3.7)
i,t 0 1 i,t i,t st i,t
(cid:124) (cid:123)(cid:122) (cid:125) (cid:124)(cid:123)(cid:122)(cid:125) (cid:124) (cid:123)(cid:122) (cid:125) (cid:124)(cid:123)(cid:122)(cid:125)
precision stability regimesufficiency OOSpersistence
where τ is estimate precision (inverse variance), π the stability-selection probability,
i,t i,t
ϕ(n
st
) = 1−e−nst /n0 ∈ [0,1]anincreasingfunctionofregimesamplesize,andρ
i,t
theOOS
persistenceratio. Eachtermlivesin[0,1](precisionsquashedthroughalogisticσ),sothe
productisinterpretable: confidenceishighonlywhentheestimateispreciseandstable
and backed by enough regime data and replicates out of sample. Any single weak link
pullsitdown. Thatmultiplicativefragilityisafeature: itencodesappropriatehumility.
3.4.3 Theoperationalcoupling: confidence-shrunkrelevance
Thesystemactsonneither RnorCalonebutonaconfidence-shrunkeffectiveweight. This
iswherepartialpooling/shrinkagetowardaskepticalpriorenters: whenconfidenceislow,we
shrinkthesource’sinfluencetowardthepriorbeliefthatitisirrelevant.
w = R ·g(C ), g(C) = Cγ (3.8)
i,t i,t i,t
withγ ≥ 1controllinghowaggressivelylow-confidencesourcesaresuppressed. AsC → 0,
i,t
w → 0: anuntrustedsourceissilenced,nomatterhowlargeitsrawrelevance. Thisisthe
i,t
mathematicalstatementof“watch,don’tsize,”andthesinglemostimportantequationfor
real-worldsurvival—itmakesthesystemautomaticallyconservativeinexactlythesituations
whereadaptivesystemsblowup: newregimes,thindata,unstableestimates.
41

AdaptiveMean-ReversionProgramme TheConditionalRelevanceEngine
3.5 Whyrelevancemustevolve,andwhenitstops—thetheoreticalanchors
Thethreeanchorpapersarenotdecoration;eachsuppliesoneload-bearingargument.
3.5.1 AdaptiveMarketsHypothesis—whyrelevanceevolvesatall
Loreframesmarketefficiencyasanevolutionary,ecologicalproperty: profitopportunities
appear, get competed away as participants adapt, and disappear — like niches in nature.
Theimplicationisdecisive: afixedrelevancerankingistheoreticallyincoherent. Ifasignal
reliablypredictedmean-reversionforever,itwouldbearbitragedintoirrelevance. Thevery
factthatweexpectsignalstoworkimplieswemustexpecttheirusefulnesstodecayandrotate.
Thisiswhy R carriesatimesubscriptandwhytheforgettingfactorλisnotahackbuta
i,t
theoreticalnecessity. AMHalsojustifiesregimeconditioning: differentecologieshostdifferent
exploitablestructures. Andittellsuswhatnottobuild: ifrelationshipsevolve,anenormous
static model fit once on all history is exactly wrong; a smaller, continuously-reweighted
systemisright. AMHisthetheoreticallicenseforoursimplicitypremium.
3.5.2 Time-varyingpredictabilityliterature—wheninformationstopsmattering
Theempiricalforecastingliteraturesuppliestheoperationalcounterpart: predictiverelation-
shipsareunstable,regime-andbusiness-cycle-dependent,andfrequentlyin-sample-only.
Threedesignrulesfallout. (1)Out-of-sampleistheonlyhonesttest—hence ∆ isdefined
i,t
onOOSloss,andρ isaconfidencedriver. (2)Predictorsswitchoff—“whendoesinforma-
i,t
∆
tionstopmattering?” hasaconcreteanswer: when decays(forgettingletsitfade)and/or
i,t
whentheregimechanges(changepointresetstheconditioning). Wedonotneedtopredicta
signal’sdeath;weneedanestimatorthatnoticesitquickly. (3)Combine,don’tconcentrate—
carrymanysourceswithconfidence-shrunkweightsandaverage,ratherthanbettingona
single“best”signal.
3.5.3 LópezdePrado—howtoavoidspuriousrelevance
Methodologicalhygiene. Substitutioneffects: whentwofeaturesshareinformation,naive
importancemisattributescredit;hisclusteredfeatureimportancegroupscorrelatedfeatures
and scores the cluster — we adopt this, so R does not double-count. MDA over MDI:
∆
permutation, out-of-sample importance is preferred to in-sample impurity; our is an
i,t
MDA-in-spiritquantity. Meta-labelling: separatingdirectionfromsizingmapsontoour R/C
split. Multiple-testingawareness: stabilityselection’sfinite-samplefalse-discoverycontrol
isourdefenseandfeedsdirectlyintoC .
i,t
Together: Lo says relevance must move, the forecasting literature says it must be
judgedout-of-sampleandcombined,andLópezdePradosayswemustmeasureit
withoutfoolingourselves. Theframeworkistheminimalobjectthathonorsallthree.
3.6 Candidatemathematicaltools—honestevaluation
Each method scored against the project’s filters — intuition, mathematics, assumptions,
overfitting risk, real-time feasibility, robustness under regime instability, interpretability,
compatibility with the stack. The verdict states whether it is in the core, retained as an
optionalcross-check,orexcluded.
42

AdaptiveMean-ReversionProgramme TheConditionalRelevanceEngine
|     |     | Keystrength/weakness | Verdict |
| --- | --- | -------------------- | ------- |
Method
|     |     | directlyourdefinition;interpretable,cheap/ | CORE |
| --- | --- | ------------------------------------------ | ---- |
Exp-weightedincremental
needsatargetlabel
OOSskill(∆)
|                    |     | FDRcontrol,robustness,givesπ/costofmany | CORE(confidence) |
| ------------------ | --- | --------------------------------------- | ---------------- |
| Stabilityselection |     | refits                                  |                  |
|                    |     | adaptivity=AMHrequirement/λtuning       | CORE(adaptivity) |
Forgettingfactor/DMA
|          |                | real-timeregimereset,principled/hazard-prior | CORE(condition- |
| -------- | -------------- | -------------------------------------------- | --------------- |
| Bayesian | online change- | choice                                       | ing)            |
point(BOCD)
|     |     | tamesthin-dataregimes/priorspecification | CORE(viag(C)) |
| --- | --- | ---------------------------------------- | ------------- |
Shrinkage/partialpooling
|             |               | capturesnonlinearity/data-hungry,biased | CROSS-CHECK |
| ----------- | ------------- | --------------------------------------- | ----------- |
| Conditional | mutual infor- |                                         |             |
mation
|     |     | directionalinfoflow/verydata-hungry,noisy | CROSS-CHECK |
| --- | --- | ----------------------------------------- | ----------- |
Transferentropy
|       |           | robust>singlemodel/weightscanchurn | CORE(aggrega- |
| ----- | --------- | ---------------------------------- | ------------- |
| Model | averaging |                                    | tion)         |
(BMA/DMA)
|           |                | killssubstitutiondouble-counting/clustering | CORE(preprocess- |
| --------- | -------------- | ------------------------------------------- | ---------------- |
| Clustered | feature impor- |                                             |                  |
|           |                | choice                                      | ing)             |
tance
Foldedinto∆
model-agnostic,OOS/correlated-featuredistor-
| Permutation | importance | tion |     |
| ----------- | ---------- | ---- | --- |
(MDA)
|     |     | cheap/in-sample,misleading | EXCLUDED |
| --- | --- | -------------------------- | -------- |
MDI/in-sampletreeimpor-
tance
|               |             | flexible/black-box,fragileOOS | EXCLUDED |
| ------------- | ----------- | ----------------------------- | -------- |
| Deep learning | / attention |                               |          |
importance
|                       |     | goldstandardifachievable/infeasibleinmar- | EXCLUDED(weak |
| --------------------- | --- | ----------------------------------------- | ------------- |
| Strictcausaldiscovery |     | kets                                      | proxy)        |
Thereasoningbehindthecuts. Informationtheoryisacross-check, notthecore—CMIand
transferentropymeasureexactly“incremental,nonlinear,directionalinformation,”butthey
areestimationnightmaresinourlow-data,single-young-regimesetting;wekeepthemas
a periodic offline validator. Deep learning and black-box importance are excluded — they fail
interpretability,overfitting-resistance,andlimited-datafiltersatonce. Strictcausalityisdown-
ranked—genuineinterventionalcausalityisnotidentifiableinobservationalmarketdata;
pretendingotherwiseproducesfalseconfidence,theworstfailureforaconfidence-scoring
system. Thecoreissmall: everythingintheCORErowscomposesintoonerecursiveestimator
withoneconfidencescore.
3.7 Thecommittedminimalframework(formalspecification)
Thissectionistheimplementablespec,writtensothatacompetentengineercouldbuildthe
firstversionfromit. WecallittheConditionalRelevanceEngine(CRE).
43

AdaptiveMean-ReversionProgramme TheConditionalRelevanceEngine
3.7.1 Inputstheengineassumes
▶ Candidatesources x ,...,x —theinformationstreamswhoserelevancewejudge
|     |     |     | 1,t | N,t |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
µ∗,
(deviation from volatility state, volume signals, MRScore/DRC sub-components,
term-structurevariables,etc.).
▶ Regimestates andrun-lengthr —suppliedbytheregimelayer. WerecommendBOCD
|     |     | t   |     |     | t   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
forr (timesincethelaststructuralbreak),becauseitisonlineandgivesaposteriorover
t
run-length,whichfeedsconfidencedirectly.
▶ TargetlabelY —theMR-outcomemeta-label: givenadeviationbeyondthresholdat
t
timet,didpricereverttowardµ∗ byatleastκ withinhorizonh? (Binary;asigned/contin-
uousP&Lvariantisadrop-inalternative.)
| 3.7.2 Preprocessing: |     |     | clustertodefeatsubstitution |     |     |     |     |     |     |     |     |
| -------------------- | --- | --- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Beforescoring,groupthe N sourcesintoclusters{G ,...,G }ofcorrelatedstreams(hier-
|     |     |     |     |     |     |     | 1   | K   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
archicalclusteringonarobustdependencematrix,refreshedslowly). Relevanceisscored
attheclusterlevel,thenoptionallyattributedwithinacluster. ThisistheLópezdePrado
clustered-importance fix and it is what makes the incrementality requirement real rather
thannominal.
3.7.3 Step1—per-windowincrementalskill
Withinthecurrentregime’srecentdata,fittwolightweightpredictivemodelsforY onan
out-of-sample(walk-forwardorpurgedk-fold)basis: abasemodelY ∼ B (existingtrusted
info)andanaugmentedmodelY ∼ B∪G . Recommendedmodelclass: regularizedlogistic
k
regression—interpretable,cheap,robust,economicallyreadablecoefficients. Compute
|     |     |     | ∆   | = L | (Y | B) | − L | (Y | B,G | ),  |     |     | (3.9) |
| --- | --- | --- | --- | --- | ------- | --- | -------- | --- | --- | --- | ----- |
|     |     |     | k,t |     | OOS     | OOS |          | k   |     |     |       |
L =
with OOS log-loss. Purge and embargo around label horizons to prevent leakage —
non-negotiableforhonestOOSnumbers.
3.7.4 Step2—adaptiverelevance(forgetting)
| Standardize | ∆   | withinregimeto |      | ∆˜    | andupdate   |     |       |             |        |         |        |
| ----------- | --- | -------------- | ---- | ----- | ----------- | --- | ----- | ----------- | ------ | ------- | ------ |
|             | k,t |                |      |       | k,t         |     |       |             |        |         |        |
|             |     | =              | (1−λ | )∆˜   | +           |     | =     | (cid:0) 1−e | −rt/r0 | (cid:1) |        |
|             | R   | k,t            |      | t k,t | λ t R k,t−1 | ,   | λ t λ | max         |        | .       | (3.10) |
The forgetting factor is low (fast forgetting) right after a detected changepoint and rises
towardaceilingastheregimematures. Thismakestheenginere-learnquicklyafterabreak
andstabilizewithinasettledregime—thepreciseadaptivebehaviorAMHdemands.
3.7.5 Step3—thefourconfidencecomponents
∆
Precision: σ(β +β τ ), τ = inversevarianceof acrossOOSfolds; (3.11)
|     |     | 0   | 1 k,t | k,t |     |     | k,t |     |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
Stability: π = fractionofsubsampleswhereG isretained(stabilityselection, Brefits);
|     |     | k,t |     |     |     |     | k   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(3.12)
−nst /n0,
Sufficiency: ϕ(n ) = 1−e n = effectivesampleincurrentregime; (3.13)
|              |     | st       |              |      | st      |     |     |     |     |     |        |
| ------------ | --- | -------- | ------------ | ---- | ------- | --- | --- | --- | --- | --- | ------ |
|              |     |          | (cid:0)∆OOS/ |      | (cid:1) |     |     |     |     |     |        |
|              |     | =        |              | ∆IS, |         |     |     |     |     |     |        |
| Persistence: | ρ   | k,t clip |              |      | 0, 1 .  |     |     |     |     |     | (3.14) |
|              |     |          | k,t          | k,t  |         |     |     |     |     |     |        |
44

AdaptiveMean-ReversionProgramme TheConditionalRelevanceEngine
Combinemultiplicatively:
|     |     | =   | σ(β | +β      | ) · | · ϕ(n | ) ·      | ∈ [0,1]. |        |
| --- | --- | --- | --- | ------- | --- | ----- | -------- | -------- | ------ |
|     | C   | k,t | 0   | 1 τ k,t | π   | k,t   | st ρ k,t |          | (3.15) |
3.7.6 Step4—confidence-shrunkweightandaggregation
|     |     |     |     | w = | max(R | ,0)·C | γ . |     | (3.16) |
| --- | --- | --- | --- | --- | ----- | ----- | --- | --- | ------ |
|     |     |     |     | k,t |       | k,t   |     |     |        |
k,t
Wefloorrelevanceatzero: negativeincrementalskillmeans“ignore,”not“tradetheoppo-
| site,”whichwouldbeover-fittingnoise. |     |     |     |     | Normalizeacrossclusters: |     |     |     |     |
| ------------------------------------ | --- | --- | --- | --- | ------------------------ | --- | --- | --- | --- |
w
|     |     |     |     | wˆ  | =   | k,t | .   |     | (3.17) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
|     |     |     |     | k,t | ∑   |     |     |     |        |
w +ϵ
j j,t
The +ϵ matters: when nothing is both relevant and trusted, all wˆ → 0 and the system
correctlysays“noinformationcurrentlyqualifies”ratherthanforcingspuriousweightsto
sumtoone. This“permissiontoabstain”isarobustnesspropertymostweightingschemes
lack.
3.7.7 Theengineinpseudocode
| for each timestamp |                                     | t:                 |           |               |            |               |             |            |     |
| ------------------ | ----------------------------------- | ------------------ | --------- | ------------- | ---------- | ------------- | ----------- | ---------- | --- |
| s_t, r_t           | = RegimeLayer.update(market_data_t) |                    |           |               |            |               | # BOCD      | run-length |     |
| lambda_t           | = lambda_max                        |                    | *         | (1 - exp(-r_t |            | / r0))        |             |            |     |
| clusters           | = cluster_sources(sources_t)        |                    |           |               |            |               | # slow      | refresh    |     |
| for each           | cluster                             | G_k:               |           |               |            |               |             |            |     |
| # Step             | 1: incremental                      |                    |           | OOS skill     | (purged    | walk-forward) |             |            |     |
| L_base             | = oos_logloss(Y,                    |                    |           | base_set;     |            | regime=s_t)   |             |            |     |
| L_aug              | = oos_logloss(Y,                    |                    |           | base_set      | + G_k;     | regime=s_t)   |             |            |     |
| delta              | = L_base                            |                    | - L_aug   |               |            |               |             |            |     |
| delta_z            | = standardize_within_regime(delta,  |                    |           |               |            |               | s_t)        |            |     |
| # Step             | 2: adaptive                         |                    | relevance |               |            |               |             |            |     |
| R[k]               | = (1 -                              | lambda_t)          |           | * delta_z     | + lambda_t |               | * R_prev[k] |            |     |
| # Step             | 3: confidence                       |                    |           |               |            |               |             |            |     |
| tau                | = precision_from_folds(delta)       |                    |           |               |            |               |             |            |     |
| pi                 | = stability_selection_prob(Y,       |                    |           |               | base_set,  |               | G_k, s_t)   |            |     |
| phi                | = 1 -                               | exp(-n_regime(s_t) |           |               | / n0)      |               |             |            |     |
| rho                | = clip(delta_oos                    |                    |           | / delta_is,   | 0,         | 1)            |             |            |     |
| C[k]               | = sigmoid(b0                        |                    | + b1*tau) | *             | pi * phi   | * rho         |             |            |     |
| # Step             | 4: effective                        |                    | weight    |               |            |               |             |            |     |
| w[k]               | = max(R[k],                         |                    | 0) *      | C[k]**gamma   |            |               |             |            |     |
w_hat = normalize(w) # sums to <=1; abstains when nothing qualifies
| emit({cluster: |     | (R[k], | C[k], | w_hat[k])}) |     |     |     |     |     |
| -------------- | --- | ------ | ----- | ----------- | --- | --- | --- | --- | --- |
3.7.8 Parametersandhowtosetthem(allinterpretable)
45

AdaptiveMean-ReversionProgramme TheConditionalRelevanceEngine
Meaning Sensible Setby
Param default
maxmemoryinasettledregime 0.97 howpersistent
λ max regimesare
run-lengthscaleforre-learning ∼1regime regimelayerstats
r 0 half-life
sampleneededbeforetrustinga ∼30–60events labelfrequency
n 0 regime
stabilitysubsamples 100 computebudget
B
confidenceaggressiveness 2 riskappetite(higher
γ =moreconservative)
labelhorizon/reversionthresh- fromµ∗ tradedefinition
h,κ old dynamics
Every parameter has a finance meaning. There are no opaque hyperparameters, which
satisfies the interpretability filter and makes the system auditable — a quant can defend
everynumbertoaportfoliomanager.
3.8 HowtheCREplugsintotheexistingstack
Theengineisdesignedtoconsumethefrozenlayersandservetheliveones,withoutreopening
settledquestions.
▶ MRScore / DRC (Layer 1). DRC sub-components become candidate sources. The CRE
answers “which DRC inputs currently carry incremental information in this regime,”
refining(notreplacing)thefrozenMRScore.
▶ Regimedetection(Layer2). Thetightestcoupling. TheCREneedss andr fromthislayer,
t t
andinreturnitoperationalizestheLayer-2thesis: “signalsthatbehaveabnormallybefore
atransition.” AsignalthatearnsrisingRandCaheadof aconfirmedMRScoreacceleration
ispreciselyanearly-warningsource—thealpha-before-the-crowdthemandateseeks.
TheCREturnsthathypothesisintoameasurablequantity.
▶ Equilibriumµ∗ (Layer3). Thecompetingµ∗ estimatorsarethemselvescandidatesources;
theCRE’s R/Cmachineryisthenaturalarbiterof“whichequilibriumestimateismost
usefulinthisregime”—exactlytheopenquestionintheµ∗ workingpaper. Sameengine,
differentinputs.
▶ Marketclassification(Layer4). Theregimelabels canbeenrichedbytheclassification
t
layer;theCREconsumeswhateverconditioningtheclassifierprovides.
▶ Signal generation (Layer 5). Deliberately downstream. The CRE outputs {(R,C,wˆ)};
signalgenerationconsumesthemlater. Wearenotgeneratingsignalshere,honoringthe
sequencingrule.
Theunifyingpayoff
Relevance,equilibrium-selection,andearly-warningallbecomethesamemathemat-
icalquestion—incremental,regime-conditional,confidence-weightedusefulness—
expressibleinoneengine.
46

AdaptiveMean-ReversionProgramme TheConditionalRelevanceEngine
3.9 Anti-overfittingandvalidationprotocol
Aconfidence-scoringsystemthatisitselfoverfitisworsethanuseless. Safeguards,inorder
ofimportance: (1)EverythingOOS— ∆ , ρ,andstabilityareallcomputedout-of-sample
with purging and embargoing around label horizons; no in-sample importance metric is
evertrusted. (2)StabilitygatewithFDRcontrol—sourcesthatdon’tcleartheselection-
probabilitythresholdgetnear-zeroconfidenceregardlessofpointestimate. (3)Cluster-level
scoring—defeatssubstitution-drivenfalseimportance. (4)Multiplicativeconfidence—
a single failure mode (thin regime, unstable estimate, OOS collapse) zeroes confidence;
thesystemerrstowardabstention. (5)Walk-forward/combinatorial-purgedCVforany
parametertuning;reportdeflatedperformance. (6)Regime-out-of-sampletest—validate
thatrelevanceestimatedinhistoricalregimesoftypeAtransferstoheld-outregimesoftype
A.(7)Negativecontrols—injectpure-noise“sources”;acorrectenginemustassignthem
low RandlowC.
3.10 Failuremodesandhonestlimitations
▶ Labeldependence. EverythingisanchoredtoY. Apoorly-specifiedlabel(h,κ wrong)
corrupts all relevance. Mitigation: treat label design as a first-class research task; test
sensitivitytoh,κ.
▶ Cold-startinnewregimes. Rightafterachangepoint, n istiny,soconfidenceis(cor-
st
rectly)lowandthesystemisnear-silent—safe,butleastusefulexactlywhenregimes
areyoungest,whichmaybewhenMRopportunityisrichest. Thisisarealtension. Partial
fix: borrowstrengthfromanalogoushistoricalregimesviahierarchicalpooling—the
highest-valueextension.
▶ Linear workhorse blind spots. Logistic/linear incremental skill can miss genuinely
nonlinear relevance. Mitigation: the CMI / transfer-entropy cross-check catches this
offline;ifitsystematicallydisagrees,upgradetheworkhorselocally.
▶ Regime mislabeling propagates. If the regime layer is wrong, conditioning is wrong.
Mitigation: BOCD’srun-lengthposteriorletsussoftenconditioning(probabilisticmem-
bership)ratherthanhard-assign.
▶ Forgetting-factorwhipsaw. Too-fastforgettingchasesnoise; too-slowmissesrotation.
Mitigation: monitorrelevancechurnasadiagnostic.
▶ Non-stationary confidence. Even confidence estimates can be unstable; we do not
currentlyhavea“confidenceintheconfidence.” Acceptableforv1—asecondmeta-layer
wouldviolatethesimplicitypremium.
3.11 Implementationroadmap(minimumviableenginefirst)
Sequencedsoeachstepisindependentlytestable:
1. DefineandvalidatetheMR-outcomelabelY (dependsonµ∗). Nothingelseismeaningful
untilthisissolid.
2. Build the incremental-skill core ( ∆ via purged walk-forward logistic). Validate on
negativecontrols.
3. Addforgetting(R recursion),fixedλfirst,thenrun-length-tied.
k,t
4. Add confidence, one component at a time, in order of value: stability π → regime
sufficiencyϕ→OOSpersistenceρ →precisionτ.
47

AdaptiveMean-ReversionProgramme TheConditionalRelevanceEngine
5. Addclusteringpreprocessing.
6. Wireintheregimelayer(s ,r )forconditioning;beforethat,runsingle-regimetodebug.
t t
7. Aggregation+abstention(wˆ).
8. Cross-checkharness(offlineCMIagreement)—last,optional.
Shipafterstep4onasingleregimeasaresearchprototype;everythingafterishardening.
3.12 Openquestions
1. Labeldesign. Binaryreversionvs.signedP&Lvs.continuousreversionfraction—which
targetmakesrelevancemoststable? Highest-leverageopenitem.
2. Hierarchical pooling across regimes. Can we borrow strength from analogous past
regimestosolvecold-startwithoutoverfitting? Themostpromisingextension.
3. Probabilistic(soft)regimeconditioningusingBOCD’sfullrun-lengthposteriorinstead
ofahards .
t
4. Clusterattribution. Howtoattributeclusterrelevancebacktoindividualsourceswithout
reintroducingsubstitutionbias.
5. Confidencecalibration. Dorealizedoutcomesmatchstatedconfidence? Areliability-
diagramdisciplineforC.
3.13 Closing—didwemeetthesuccesscriterion?
Themandate’ssuccesstestwasthatwecouldfinallysay: “Wenowknowhowtomathematically
estimatewhichinformationmatteredinamarket/regimeandhowconfidentweareinthatestimate.”
Wecannowanswerbothhalvesconcretely.
Theanswer
Whichinformationmattered: theregime-conditional,exponentially-weighted,out-of-
sampleincrementalskill R ofeach(clustered)sourceagainsttheMR-outcomelabel.
i,t
How confident we are: the multiplicative score C combining estimate precision,
i,t
resamplingstability,regimesamplesufficiency,andout-of-samplepersistence—fused
into a confidence-shrunk weight w = R g(C ) that silences what we do not yet
i,t i,t i,t
trust.
Itisminimal,interpretable,adaptivebyconstruction(AMH),out-of-samplebydiscipline
(forecastingliterature),andspurious-resistantbydesign(LópezdePrado). Itsurvivesthe
project’sfilters. Empiricalimplementationcannowbegin—startingwiththelabel.
48

Part IV
| Glossary | & Mathematical | Appendix |
| -------- | -------------- | -------- |
49

APPENDIXA
Glossary & Mathematical Appendix
Thisappendixmakesthedossierself-contained. Atechnicallysophisticatedreaderwithnopriorexposure
totheprogrammeshouldbeabletoreconstructtheentireframeworkfromit. Ithasfourparts: asymbol
table,aformulaglossary(intuition,variables,purpose,role),amethodologyglossary(problemsolved,
strengths,weaknesses,assumptions,whychosen,alternatives),andakey-conceptglossary.
A.1 Symboltable
Symbol Meaning
P Observedpriceattimet.
t
µ∗ Latentequilibrium(“fair”)priceatt,estimatedbytheAnchoredKalman
t
filter. Theobjectpricerevertstoduringamean-revertingregime.
ε Theresidualordeviation,ε = P −µ∗. Thecentraltradedquantity: afade
t t t t
betsεshrinks.
z, z Standardiseddeviationz = ε/σ;z istheentrythreshold(|z| ≥ z
entry entry entry
requiredtoconsiderafade).
ϕ AR(1)persistencecoefficientoftheresidual;ϕ → 1isthenear-unit-root
(trend)regime.
κ Mean-reversionspeed,κ = −lnϕ. Largeκ =fastreversion. Hardto
estimateneartheunitroot.
σ Innovation(shock)standarddeviationoftheresidualprocess—a
η
volatility,notareversion,parameter.
σRV Realised-volatilityscaleofabar,usedtosetprofit/stopbarriers(e.g.
g ≈ 0.5σRV,s ≈ 1.0σRV).
b(z,t) Netpressure: theconditionaldriftoftheresidual, E[∆ ε | ε,state]. Its
zero-crossingdefinesStateT’signition.
H, h Trade/labelhorizon(barswithinwhichreversionmustoccur).
s , r Regimestateattanditsrun-length(timesincethelastchangepoint),
t t
fromtheregimelayer(BOCD).
Y TheMR-outcomelabel: didastretcheddeviationrevertby≥ κ withinh?
t
Thetargetrelevanceisanchoredto.
x Candidateinformationsourceiatt.
i,t
G Clusterkofcorrelatedsources(relevanceisscoredpercluster).
k
50

AdaptiveMean-ReversionProgramme Glossary&MathematicalAppendix
| Symbol | Meaning |     |     |     |
| ------ | ------- | --- | --- | --- |
B
| t   | Baseinformationsetalreadytrusted/inuseatt. |     |     |     |
| --- | ------------------------------------------ | --- | --- | --- |
| I   | Fullcandidateinformationsetatt.            |     |     |     |
t
| L   | Out-of-samplepredictiveloss(log-lossforbinaryY). |     |     |     |
| --- | ------------------------------------------------ | --- | --- | --- |
∆ , ∆ IncrementalOOSskillofsourcei/clusterk: lossreductionfromadding
i,t k,t
ittoB. Theatomofrelevance.
R , R Relevance: exponentially-weighted,regime-standardisedincremental
i,t k,t
skill.
| C , C | Confidence: | trustintherelevanceestimate,in[0,1]. |     |     |
| ----- | ----------- | ------------------------------------ | --- | --- |
i,t k,t
|               |                                        |     | g(C ).    |                       |
| ------------- | -------------------------------------- | --- | --------- | --------------------- |
| w i,t , w k,t | Confidence-shrunkeffectiveweight,      |     | R i,t i,t |                       |
| wˆ            | Normalisedweightacrossclusters(sumsto≤ |     |           |                       |
| k,t           |                                        |     |           | 1;abstainswhennothing |
qualifies).
| λ, λ | Forgettingfactor(memory);λ | riseswithregimerun-length. |     |     |
| ---- | -------------------------- | -------------------------- | --- | --- |
| t    |                            | t                          |     |     |
τ Estimateprecision(inversevarianceof ∆ acrossfolds)—confidence
i,t
component.
π Stability-selectionprobability(fractionofsubsamplesretainingthe
i,t
source)—confidencecomponent.
| ϕ(n ) | Regime-sufficiencyfunction1−e−nst |     | /n0                   |     |
| ----- | --------------------------------- | --- | --------------------- | --- |
| st    |                                   |     | —confidencecomponent. |     |
OOSpersistenceratio(OOSskill/ISskill),clippedto[0,1]—confi-
ρ i,t
dencecomponent.
| γ   | Confidenceaggressivenessexponentin |     | g(C) = | Cγ (γ ≥ 1). |
| --- | ---------------------------------- | --- | ------ | ----------- |
n , r , B Regime-sufficiencyscale;run-lengthscale;numberofstabilitysubsam-
0 0
ples.
| β ,β | Logistic-squashparametersmappingprecisionτ |     |     | into[0,1]. |
| ---- | ------------------------------------------ | --- | --- | ---------- |
0 1
Equilibrium-validitygate(1ifµ∗
| V   |     |     | iscurrentlytrustworthy). |     |
| --- | --- | --- | ------------------------ | --- |
t
A.2 Formulaglossary
For each formula: intuition (what it says in words), variables, purpose / why it exists, and
implementationrole.
A.2.1 Theresidual(thetradedobject)
= P −µ ∗
ε t t t .
Intuition. Howfarpricehasstrayedfromitsestimatedfairvalue. Variables. P t observed
µ∗
price; equilibrium estimate. Purpose. Everything the programme trades is a bet on ε
t
Implementationrole.
shrinking;itisthesinglequantityallfivelayersultimatelyreference.
ComputedeachbarfromtheAnchoredKalmanµ∗;standardisedtozforthedeviationgate.
Caveat(PartI):ifµ∗lags,εcanrevertsimplybecauseµ∗catchesup—theconstructionillusion,
whichtheacausal-benchmarktest(E5)existstoexpose.
51

AdaptiveMean-ReversionProgramme Glossary&MathematicalAppendix
A.2.2 AR(1)varianceidentity—theCSUdouble-countingproof
σ2
η
Var(ε) = . (1.1)
1−ϕ2
Intuition. Foramean-revertingAR(1)residual,thespreadofdeviationsandthepersistence
ϕarethesamefactuptotheshocksizeσ . Variables. ϕpersistence;σ innovationvolatility.
η η
Purpose. Itprovesthat“AR(1)↓andvariance↓”arenottwoconfirmationsbutone—and
thattheonlyindependentpartofvarianceisσ ,avolatilitysignal. Implementationrole. The
η
reasonthecritical-speeding-upaxisisdemoted: neverfeedAR(1)anddeviation-variance
astwofeatures;ifvarianceisusedatall,useitasanexplicitvolatilitycontrol.
A.2.3 Netpressureandtheignitioncondition
b(z,t) = E[∆ ε | ε,state], ignition: b(z,t) = 0thenb·sign(ε) < 0. (1.2)
Intuition. “Pressure”iswhichwaythedeviationis,onaverage,abouttomove. Inatrend
itispushedfurtherout(b·sign(ε) > 0);ignitionisthemomentthepushflipstowardfair
value. Variables. b conditional drift; sign(ε) direction of the current deviation. Purpose.
Replacesthelossythree-partCSUsignaturewithasinglescalarfieldandacrisp,falsifiable
event(asignchange)thatisdirectlyobservablefromorderflow. Implementationrole. The
conceptualidentityofStateT;inthelivestackitscheapshadowissignedorder-flowimbalance
anditsshort-horizondrift.
A.2.4 Incrementalskill(theatomofrelevance)
∆ = L(Y | B;s )−L(Y | B,x ;s ). (3.5)
i,t t i t
Intuition. How much better we predict the trade outcome out-of-sample when we add
source i to what we already know, in this regime. Variables. L OOS loss; B base set; x
i
candidate;s regime;Y outcomelabel. Purpose. Operationalises“mattering”asincremental,
t
conditional,out-of-samplecontribution—killingdouble-countingandin-sampleillusionsin
onedefinition. Implementationrole. Computedperclusterviatwopurged/embargoed
logisticfits(basevs.augmented);theinputtotherelevancerecursion.
A.2.5 Relevancerecursion(adaptivity)
R
i,t
= (1−λ)∆˜
i,t
+λR
i,t−1
, λ
t
= λ
max
(cid:0) 1−e −rt/r0 (cid:1) . (3.6,3.10)
Intuition. Smooth the noisy per-window skill into a running estimate that forgets old
evidence;forgetfastjustafteraregimebreak,slowlyoncetheregimehassettled. Variables.
∆˜ regime-standardised skill; λ memory; r run-length. Purpose. Encodes the Adaptive
t
MarketsHypothesis: relevancemustdecayandrotate,andthesystemmustre-learnaftera
break. Implementationrole. Onelineofstatepercluster;sameshapeastheKalman/DMA
updatesalreadyinthestack,soitcomposescleanly.
A.2.6 Confidence(multiplicativetrust)
C = σ(β +β τ )·π ·ϕ(n )·ρ . (3.7)
i,t 0 1 i,t i,t st i,t
Intuition. Trusttherelevanceestimateonlyifitispreciseandstableunderresamplingand
backed by enough regime data and it replicates out of sample. Any one failure collapses
trust. Variables. τ precision; π stability-selectionprobability; ϕ(n )regimesufficiency; ρ
st
OOS persistence. Purpose. Separates how strong a signal looks from how much we believe
the measurement — the conceptual core of the engine. Implementation role. Four cheap,
52

AdaptiveMean-ReversionProgramme Glossary&MathematicalAppendix
separately-loggablenumbers;themultiplicativeformmakesthesystemabstaininexactly
theconditionswhereadaptivesystemsblowup.
A.2.7 Confidence-shrunkweightandaggregation
w
w = max(R ,0)·C γ , wˆ = k,t . (3.8,3.17)
i,t i,t i,t k,t ∑ w +ϵ
j j,t
Intuition. Actonrelevanceonlytotheextentyoutrustit; ifnothingisbothrelevantand
trusted,putonnothing. Variables. γconservatism;ϵabstentionguard. Purpose. Thesingle
mostimportantequationforsurvival—itsilencesuntrustedsourcesandgrantsthesystem
“permissiontoabstain.” Implementationrole. TheCRE’soutputconsumedbydownstream
sizing;themax(·,0)floorpreventstradingtheoppositeofanoisynegativeskill.
A.2.8 Costedtriple-barrierlabelandtheeconomichurdle
Y = 1{revert ≥ κ withinh}, E[netfadeP&L] > hurdle ≈ 5–6bpsroundtrip.
t
Intuition. A fade “worked” only if it gave back enough of the deviation, fast enough, to
clear costs — with a profit target g ≈ 0.5σRV against a stop s ≈ 1.0σRV. Purpose. Forces
economicsignificanceoverstatisticalsignificance: theflooris∼anorderofmagnitudeabove
the statistical-significance floor, demanding a hit rate above ∼2/3. Implementation role.
BoththetrainingtargetY forthehazardandthescoringmetricforeveryrelevancelayer
(OOSeconomicvalue).
A.3 Methodologyglossary
For each methodology: what problem it solves, strengths, weaknesses / assumptions, why we
selected(orrejected)it,andalternativesconsidered.
A.3.1 AnchoredKalmanfilter(equilibriumestimation,µ∗)
Problem. Estimatealatent,slowly-movingequilibriumpriceonline,withanuncertainty
estimate. Strengths. Producesaconfidence/variancenatively(neededforsizing);anchored
to VWAP to resist drift; supports CUSUM break detection. Weaknesses / assumptions.
Gaussian innovations and a chosen process variance Q; a lagging filter can manufacture
apparent reversion (the construction illusion). Why selected. Chosen over rolling mean
/ EMA (no uncertainty, trend contamination, EMA is an ARMA(1,1) sub-case), over OU-
implied equilibrium (near-unit-root variance ∼104×, useless at n = 60), and over S/R
midpoints (lookahead). Alternatives. HMM (rejected as the equilibrium engine — zero-
width-jump transitions); particle filter (reserved for a jump-augmented-OU extension);
adaptive-Qvariants(deferreduntilthefixed-Qbaseisvalidated).
A.3.2 MRScore/DRC(Layer1detection)
Problem. Decide whether a market has historically been favourable for mean reversion,
and whether it empirically reverts. Strengths. Simple, interpretable 3-block score with
deliberatelyfixedeconomic-priorweights(20/60/20)thatresistoverfitting;DRC(forward-
return-on-zregressionwith β < 0)isacleanvalidationanchor. Weaknesses. Unconditional
andinstrument-level—slow,andsilentonwhythecurrenttrendexists. Whyselected. It
is the favourability filter and the metric everything else validates against. Alternatives /
relationship. It does not substitute for the etiology gate, which is fast, conditional, and
episode-level;thetwoareorthogonalandbothneeded.
53

AdaptiveMean-ReversionProgramme Glossary&MathematicalAppendix
A.3.3 Trend-etiologyclassifier(themissinglayer)
Problem. Determinewhythecurrenttrendexists,becauseStateT’sflow-exhaustionmech-
anism only exists in flow/inventory/behavioural trends — not in information-repricing
trends,wheretheequilibriumitselfmoved. Strengths. Thesinglehighest-valueaddition;
gatesouttheetiologieswherefadinglosessystematically. Weaknesses/assumptions. Labels
arenoisy;acoarseruleversionrisksmisclassifyingambiguouscases. Whyselected(rule-
based v0). At low base rates a learned classifier would overfit and break interpretability;
a3-wayrule({flow/behavioural,information-repricing,ambiguous})fromcheapproxies
(event calendar; gap-and-vol-jump; OI-build-then-stall) is falsifiable now. Decisive use.
Stratification—everybase-rateandpredictabilitystatisticiscomputedwithinbuckets,or
poolingwashestheeffectout(themostlikelyfalsenegative).
A.3.4 Discrete-timehazard/survivalpanel+meta-labelling
Problem. Modelatime-varyingprobabilityofanonsetevent,withcovariatesandcensoring,
atlowbaserates. Strengths. Interpretable;nativetocensoringandrareevents;produces
a calibrated probability for sizing; a pooled logistic is cheap and robust. Meta-labelling
separatesdirection(aprimaryrule)fromwhethertoactandhowmuch(thesecondarymodel).
Weaknesses. Asecondmodelisasecondplacetooverfit;needsenougheventstotrain. Why
selected. ItisthenaturalstatisticalhomeofStateT’s“hazard-governedonset.” Alternatives
rejected. HMM(wrongobject—zero-widthinterior);reinforcementlearning(event-starved;
memorisespaths);deepsequencemodels(data-starved;destroyinterpretability);continuous-
timeκ filtering(re-importsthenear-unit-rootestimationproblem).
A.3.5 Pressure-balancereformulation(orderflow,queuing,MFG)
Problem. Give the order-flow mechanism a rigorous generative model, a hazard, and a
reasontherecognitiongapexists. Strengths. Directlyobservablecause(signedOFIandits
drift)withdocumentedprice-impactstructure;queuingsuppliesasynthetic-ground-truth
simulator(theonlyroutetoanearlinesstest)andthehazard’sfunctionalform;MFGexplains
therecognitiongapasthemean-fieldconvergencetime. Weaknesses/assumptions. Full
queue-reactiveestimationneedsmessage-leveldata;MFGrequiressolvingacoupledHJB
/Fokker–Plancksystemwithunobservableagentcostfunctionals. Whyselected(witha
boundary). Adopt the pressure-balance framing as the identity and reduced-form OFI as
the live observable; keep queuing and MFG offline (simulation, hazard form, qualitative
gap predictions). Alternatives. The demoted CSU signature — kept only as at most one
confirmatorycovariate.
A.3.6 Elastic-netshrinkagetowardaneconomicprior(staticrelevancebackbone)
Problem. Combineasmallsetofaxeswithoutoverfittingweights. Strengths. Tamesfeature
explosionandnoise;elastic-nethandlescollinearaxesgracefully(unlikepurelasso). Weak-
nesses. Static—doesnotadapttoregimeonitsown;penaltystrengthcanbeoverfit. Why
selected. Itformalisesthespiritofthefrozen20/60/20fixed-priorchoice,withthepenalty
fixedfromtheory;itisthesafebaselinethedynamicmethodsmustbeatOOS.Alternatives.
Rollingexplanatorypower(demotedtodiagnostic—aderivativeofanoisystatistic);DMA
(deferred—event-starvedatdaily).
54

AdaptiveMean-ReversionProgramme Glossary&MathematicalAppendix
A.3.7 Partialpooling/hierarchicalshrinkage(regimeconditioning)
Problem. Useregime-localweightswithoutsplinteringthesampleintonoise. Strengths.
Wherearegimebuckethastoolittledata,estimatesfallbacktothepooled(unconditional)an-
swer—directlydefusingtheconditional-vs-unconditionaltrap. Weaknesses/assumptions.
Needsatinynumberofrobustbuckets(≤ 3);priorspecificationmatters. Whyselected. Itis
theonlyformofconditioningthatrespectstheCommodity-paperwarningthatconditioning
losttounconditionalOOS.Rule. Abucketonly“earns”itsownweightsbybeatingpooled
OOSeconomicvalue.
A.3.8 Stabilityselection(confidencecomponent)
Problem. Decidewhetherasource’srelevanceisrealoraone-sampleartifact, withfalse-
discovery control. Strengths. Subsample-and-select gives a selection probability π and
finite-sample FDR bounds. Weaknesses. Cost of many refits; a threshold choice. Why
selected. It is the resampling-stability driver of confidence and the program’s defense
against spurious relevance. Alternatives. In-sample importance (MDI) — excluded as
misleadingandsubstitution-prone.
A.3.9 Bayesianonlinechangepointdetection(BOCD,conditioning)
Problem. Supplyanonlineregimestateandarun-length(timesincethelastbreak)witha
posterior. Strengths. Real-time;therun-lengthposteriorfeedsboththeforgettingfactorλ
t
and the regime-sufficiency confidence term, and permits soft (probabilistic) conditioning.
Weaknesses/assumptions. Hazard/priorchoice;univariatebydefault. Whyselected. Itis
thelightestprincipledsourceof s andr fortheCRE.Alternatives. CUSUM(usedatthe
t t
equilibriumlevelforbreakdetection);HMMsmoothing(rejected—lookahead).
A.3.10 Information-theoreticscreens(CMI,transferentropy)—cross-checkonly
Problem. Detectincremental,nonlinear,directionaldependencemodel-free. Strengths. Con-
ceptuallyexactly“incrementalinformation,”andcatchesnonlinearitythelinearworkhorse
misses. Weaknesses. Estimationnightmaresatlowdata—biased,noisy,hardtothreshold
economically; no natural weighting output. Why retained as cross-check. As a periodic
offlinevalidator: ifCMIbroadlyagreeswiththeregression-based ∆ overlongwindows,we
gainconfidencethelinearcoreisnotmissinggrossnonlinearity. Whynotcore. Itviolates
thereal-time-feasibilityandlimited-datafilters.
A.3.11 Excludedmethods(namedtoclosethemoff)
Deeplearning/attentionimportance—black-box,data-hungry,fragileOOS;failsinter-
pretability, overfitting-resistance, andlimited-datafiltersatonce. Strictcausaldiscovery
—notidentifiableinobservationalmarketdata;producesfalseconfidence. Reinforcement
learning—needsrewarddensityinthemillionsofepisodes;theprogrammehashundreds.
MDI/in-sampletreeimportance—in-sampleandsubstitution-prone.
A.4 Key-conceptglossary
55

AdaptiveMean-ReversionProgramme Glossary&MathematicalAppendix
Concept Explanation
StateA/T/B Theregimeontology. STATE A isthetrend(continuation;donot
fade). STATE T istheearly,tradeablemean-reversionignition(the
alphawindow). STATE B isthecrowdedreversion—everyone
seesit,theedgeisgone. TheprogrammetradesTandmustdistin-
guishitfromB.
StateT(ignition) Athreshold-activatedsignchangeintheresidual’sconditional
drift,carriedbyanorder-flowpressureflip,recognisedlatebya
crowdwhosemigrationhasafinitetimeconstant. Empiricallya
probabilityfield(ahazard),notafixed-widthwindow.
µ∗ (equilibrium) Thelatentfairpricetheresidualismeasuredagainst. Therelia-
bilityofeverythingdownstreamdependsonµ∗ beingacontempo-
raneous,non-laggingestimate—hencetheacausal-benchmark
validation.
Residual/devia- P−µ∗: thedistancefromfairvalue. Afadebetsitshrinks.
tionε
MRScore/DRC TheLayer-1favourabilityfilter(hasthismarkethistoricallyre-
verted?) anditsprimarymetric(DRC:aforward-return-on-zre-
gressionwith β < 0). Slow,unconditional,instrument-level.
DRC DirectReversionCoefficient—theslopeoffuturereturnregressed
oncurrentstandardiseddeviationz; β < 0meansdeviationshave
historicallyreverted. Thevalidationanchor.
Trendetiology Whythecurrenttrendexists: flow/inventory/behavioural(ex-
haustible⇒Tcanexist)vs.information-repricing/fundamental-
shock(µ∗ itselfmoved⇒Tisabsentoratrap). Thedecisivemiss-
ingconditioningvariable;orthogonaltoMRScore.
Pressurebalance ThereframingofTasthezero-crossingofnetpressureb(z,t)—
theconditionaldriftoftheresidual. “Ignition”isthesignchange
ofbattheextremes. Moremeasurableandfalsifiablethanthe
three-partCSUsignature.
Criticalspeeding The(now-demoted)signatureκ↑,AR(1)↓,variance↓. Twoofits
up(CSU) threelegsareonefact(theAR(1)varianceidentity);thethirdisa
volatilitysignal;andthechangeinκ isbelowtheestimationnoise
floorneartheunitroot. Retainedasatmostoneconfirmatoryco-
variate.
Thefour-object Statisticalreversion⊃economicallytradeablereversion⊃early
nesting (State-T)reversion;andasuccessfulfadeisanex-postrealization,
notastate. Conditioningasignaturestudyonthewinnersisa
selectiontrap.
Recognitiongap Theleadbetweenwhenreversionconditionsformandwhenthe
crowdpricesthemin—literallythealpha. MFGidentifiesitwith
themean-fieldconvergencetime;itwidenswithdispersionin
participanthorizonsandnarrowsasparticipationhomogenises.
56

AdaptiveMean-ReversionProgramme Glossary&MathematicalAppendix
Concept Explanation
Order-flowimbal- Thereduced-form,model-lightshadowofthepressureflip(price
ance(OFI) change≈OFI/depth). Theproposedprimaryliveearlyobservable,
conditionalondatafeasibility.
CRE ConditionalRelevanceEngine—thecommittedframeworkof
PartIII.Maintains(R,C)persourceandemitsconfidence-shrunk
weights;theconnectivetissueunifyingdetection,equilibrium-
selection,andearly-warning.
Relevance R Regime-conditional,exponentially-weighted,out-of-sampleincre-
i,t
mentalskillofsourcei. “Doesaddingthis,givenwhatweknow,
improvepredictionofthetradeoutcomeinthisregime—and
doesitpersist?”
ConfidenceC Aseparate[0,1]number: howmuchwetrusttherelevanceesti-
i,t
mate. Multiplicativeacrossprecision,stability,regimesufficiency,
andOOSpersistence—anysinglefailurecollapsesit.
Confidence- w = R g(C ): thesystemactsonrelevanceonlytotheextent
i,t i,t i,t
shrunkweight itistrusted. “Watch,don’tsize”whenconfidenceislow;“permis-
siontoabstain”whennothingqualifies.
Stabilityselection Subsample-and-selecttogetaselectionprobabilityπ withfinite-
samplefalse-discoverycontrol—theresampling-stabilitydriverof
confidence.
Partialpooling Hierarchicalshrinkageofregime-localestimatestowardthe
pooledanswer,sothinbucketsfallbacktotheunconditionalre-
sult—thesafeguardagainsttheconditioningtrap.
Bayesianconfi- Theuseofposteriorprecision(inversevariance)asoneconfidence
dence component,andofBOCD’srun-lengthposteriortosoftenregime
conditioning.
BOCD BayesianOnlineChangepointDetection—suppliestheonline
regimestates andrun-lengthr thatdriveforgetting,regimesuffi-
t t
ciency,andsoftconditioning.
Regimecondition- Computingrelevancegiventhecurrentregimeratherthanglobally.
ing JustifiedbyAMH;disciplinedbytheCommodity-paperwarn-
ingthatconditioningisnotfreeandmustbeattheunconditional
baselineOOS.
Forgettingfactor Thememoryoftherelevancerecursion;tiedtorun-lengthsothe
λ enginere-learnsfastafterabreakandstabilisesinasettledregime
—themathematicalembodimentof“informationstopsmatter-
ing.”
Etiologygate/ Therequiredconditioninglayerthatclassifiestrendcauseand
stratification (decisively)stratifieseverystatisticbybucket,sotherealeffectis
notwashedoutbypooling.
57

AdaptiveMean-ReversionProgramme Glossary&MathematicalAppendix
| Concept |     | Explanation |     |     |
| ------- | --- | ----------- | --- | --- |
AdaptiveMarkets Lo’sevolutionaryviewofefficiency: opportunitiesappearandare
Hypothesis competedaway. Thetheoreticallicensefortime-varyingrelevance
andthesimplicitypremium.
Economicvs.sta- Thebarisrealised,costed,out-of-sampleP&L—roughlyanorder
tisticalsignifi- ofmagnitudeabovethestatistical-significancefloor. Agenuinebut
| cance |     | sub-costreversionisworthless. |     |     |
| ----- | --- | ----------------------------- | --- | --- |
Purged/embar- Cross-validationthatremovestrain/testoverlaparoundlabel
| goedCV |     | horizons—non-negotiableforhonestOOSnumbersgivenover- |     |     |
| ------ | --- | ---------------------------------------------------- | --- | --- |
lappingtriple-barrierlabels.
inaccessiblesignal=nonexistentsignal.
| Datafeasibility |     | Therealityfilter: |     | Decides |
| --------------- | --- | ----------------- | --- | ------- |
(E0) frequencyandwhethertheflowidentityisevenreachable;thetrue
firstgate.
A.5 Theempiricalgateataglance
Aconsolidatedviewofthecorrectedexperimentsequence,thethrough-linefromPartIand
PartII.
Decides
Step
Datafeasibility—frequency,andwhethertheliveflowidentityisreachable. Run
| E0  | first. |     |     |     |
| --- | ------ | --- | --- | --- |
Etiology-stratifiedbaserate—isthecost-clearedfadebaserateabovethefloorin
| E1  | therightbucket? |     |     |     |
| --- | --------------- | --- | --- | --- |
Clustering—istheeventseriesnon-IID(aregimetodetect)?
E2
Syntheticearliness—onsimulatedflowwithaknownflip,doesthedetectorfind
| E3  | itbeforepricereversion? |     |     |     |
| --- | ----------------------- | --- | --- | --- |
Realflowlead–lag—doestheOFI-driftsignchangeleadpositioningbuild-up?
E4
|     | Acausal-µ∗ | test—isthereversionreal,orµ∗ | catch-up? |     |
| --- | ---------- | ---------------------------- | --------- | --- |
E5
Crowdingseparation—doesthecrowdingaxisseparateearlyfromcrowded
| K4  | fades? |     |     |     |
| --- | ------ | --- | --- | --- |
Thesinglehighest-leveragenextmove. RunE0(datafeasibilityononeindexfuture)
jointly with locking the information-relevance evaluation protocol (OOS economic
valuevs.asimplebaseline). Establishthedataandthemeasuringstick,thenrunthe
| correctedgate. | Donotbuildthesignalfirst. |     |     |     |
| -------------- | ------------------------- | --- | --- | --- |
58

APPENDIXB
Consolidated References
Microstructure,orderflow,andgenerativemodels
▶ Cont, R., Kukanov, A. & Stoikov, S. (2014). The Price Impact of Order Book Events. J.
FinancialEconometrics12(1):47–88(arXiv1011.6402). —Order-flowimbalance≈price
change/depth;robust,model-light. BackstheliveOFIobservable.
▶ Cont, R., Stoikov, S. & Talreja, R. (2010). A Stochastic Model for Order Book Dynamics.
Operations Research 58(3):549–563. — Queuing model of the LOB; closed-form first-
passageprobabilities. Sourceoftheignitionhazard’sfunctionalform.
▶ Huang,W.,Lehalle,C.-A.&Rosenbaum,M.(2015). SimulatingandAnalyzingOrderBook
Data: The Queue-Reactive Model. JASA 110(509):107–122 (arXiv 1312.0563). — Markov
queuingLOBsimulator;thesynthetic-ground-truthenginefortheearlinesstest.
▶ Cardaliaguet,P.&Lehalle,C.-A.(2018). MeanFieldGameofControlsandanApplication
toTradeCrowding. Math.&FinancialEconomics(arXiv1610.09904). —Crowdingasa
mean-fieldequilibrium;convergencerate=recognitiontimeconstant.
▶ Hendershott,T.&Menkveld,A.(2014). PricePressures. JFE.—Inventorypricepressure,
∼1-dayhalf-life;thealiasingargumentforintraday.
Meanreversion,estimation,andregimes
▶ Scheffer, M. et al. (2009). Early-warning signals for critical transitions. Nature 461:53–59;
andCriticalspeedingup(arXiv1901.08084). —The(now-demoted)CSUsignature.
▶ Safari&Schmidhuber(2025). TrendsandReversion(arXiv2501.16772). —Sub-significant
reversioninsidetrends;thestatistical-but-uneconomiccase.
▶ Yu,J.(2012). Biasintheestimationofthemean-reversionparameter. J.Econometrics169:114–
122. —Near-unit-rootestimationbias;theκ noise-floorargument.
▶ Balke&Fomby(1997),ThresholdCointegration;Kapetanios,Shin&Snell(2003),ESTAR
unit-roottest. —Threshold/bandactivation.
▶ Bertram(2010);Leung&Li(2015);Avellaneda&Lee(2010);Gatev,Goetzmann&Rouwen-
horst(2006). —OUtrading,pairs/stat-arb,andcrowdingdecay.
▶ Hamilton — regime-switching; Short-Term Reversal with Futures (Quantpedia) — the
adversepublic-dataprior.
Informationrelevance,learning,anddiscipline
▶ LópezdePrado,M.AdvancesinFinancialMachineLearning/MachineLearningforAsset
Managers. — Feature importance (MDA/MDI), clustered importance, meta-labelling,
purgedCV.
▶ Meinshausen,N.&Bühlmann,P.(2010). StabilitySelection. JRSS-B.—Selectionprobability
andfinite-samplefalse-discoverycontrol;theconfidencestabilityterm.
59

AdaptiveMean-ReversionProgramme References
▶ Lo,A.TheAdaptiveMarketsHypothesis. —Whyrelevanceevolves;thesimplicitypremium.
▶ Adams,R.&MacKay,D.(2007). BayesianOnlineChangepointDetection(arXiv0710.3742).
—Run-lengthposteriorforregimeconditioning.
▶ Koop,G.&Korobilis,D.ForecastingInflationUsingDynamicModelAveraging. —DMA/
forgetting-factoradaptivity(deferredtoadenser-datafuture).
▶ Schreiber, T. (2000) and the financial transfer-entropy literature. — The directional
informationcross-check.
▶ Ahmed&Tsvetanov(2016),andthecommodity/equity-premiumreturn-predictability
literature. — Time-varying, out-of-sample, combination-forecast discipline; the five
relevancelessons.
Endofdossier.Allquantitativeclaimsremainprovisionaluntilvalidatedonlocked-outdata.Theauthorisednextactionis
E0—datafeasibility—runjointlywithlockingtherelevanceevaluationprotocol.
60

---

**FORWARD-REFERENCE NOTE (added 2026-06-02 — does not alter the dossier above).**
The **Substrate Observatory v1** (`docs/research/10_substrate_observatory.md`) is the first built
**worked example** of the observability-side guardrails this dossier draws (§2.5.1 market-character
layer vs §1.2.2/§1.3.1 episode-timing detection, FROZEN; §2.6.4 etiology-as-deferred-gate). It honors
the line concretely: 3 causal descriptors answer *"what kind of market does this RESEMBLE"* (character)
and deliberately exclude exhaustion/etiology/timing (the State-T side). It is transparent,
frozen-weight, and structurally terminal (no HMM/DL, feeds nothing downstream). Empirical relevance to
this dossier: **substrate character is scale-dependent** — at causal trailing windows of 60–500 bars,
even a macro-trending instrument reads RW-Null — so "what substrate is this?" (a State-T conditioning
input) has **no single-window answer**; it is a function of horizon. Read doc 10 before building any
State-T conditioning that assumes a static substrate label.
