have unique entries.A black dot onPatient refers to a mandatory role constraint.The counterexamplesofdatawith question marks(?)providemeans to test such constraintswhile validating themodelwith a domain expert.

Compared with ORM,E-R has the following shortcomings:

- .Itisnot closer tonatural languageforvalidationwith domain experts.
- E-R techniques generally support onlytwo-way relationships.Although n-way relationshipsinE-Rarebroken downinto two-wayrelationshipsbyintroducingintersection identities,these intersectionidentifiesseem arbitrary andnotunderstood by domainexperts.

Object-OrientedModeling.In this approach,both data andbehaviorare encapsulated within objects.Thus,object-oriented modeling wasprimarily devised for designing code of object-orientedprograms.However,thismodeling approach canbe adapted forconceptualmodelingand eventually for database design

By far,the most popular and widely used object-orientedapproach is the Unified Modeling Language (UML).The Unified Modeling Language has an array of diagram types,and class diagrams form one important type.Class diagrams can represent data structures andmay be consideredasextensions oftheE-Rtechnique.Apart from this briefmention ofUMLhere,we will postpone our detailed discussion ofUMLuntil the endof Chapter2.

## ModelingforDataWarehouse

As an IT professional, one must have worked on computer applications as an analyst,programmer,designer, or project manager. One must have been involved in the design, control,human resources,payroll,insurance claims,and so on.These applications that support therunningof thebusiness operations aresometimesknownas OLTP(online teleprocessing) systems. Although OLTP systems provide information and support for running the day-to-day business,they are not designed for analysis and spotting trends.

In the1990s,as businesses grewmore complex,corporations spread globally,and competition became fiercer,business executives became desperate for information to stay competitive and improve thebottomline.Theywantedtoknowwhichproduct linesto expand,which markets to strengthen,which new stores and industrial warehouses wouldbeworthwhile.Theybecame hungryforinformation tomakestrategic decisions. Although companies had accumulated vast quantities of data in their OLTPsystems, these systems themselves couldnot support intricate queries and analysisfor providing strategicinformation.

Datawarehousing is arecentparadigm specifically intended toprovide vital strategic information.It is a decision-support system.In a data warehouse,data has to be viewed and represented differently.Data modeling appropriate for building OLTP database systems becomes ineffective for data warehouse systems. Techniques such as entityexampletoillustratewhya differentmodelingtechniquebecomesdesirable for analysis.Wewant to aska question such as:What are the sales ofProduct A for the
