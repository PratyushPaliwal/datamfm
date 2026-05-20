E-Rmodel and find some of the notations,especially those for relationships,incomplete andimprecise.The fact-orienteddatamodelingapproach attempts to overcome some of thedeficiencies of theE-Rapproach.

Fact-OrientedModeling.Inthe1970s,an approach todata modelingarosebyviewing the information domain in terms of objects playing roles.What are roles?A role is the part played by oneobject in arelationship. Object-role modeling(ORM)is such a fact-oriented fairly wideindustry support.

Let us try to understand ORMwith an example. Consider the data use case for schedulingthe timeofdoctorsfor patientvisits.Thedomainexpert whois familiarwith this simple use case is able to verbalize the information content of this use case.The data modelermustbe able to transform this verbalization into a data modelto discuss easily and to validate the model.In this data modeling technique,the data modeler verbalizes sample data as instances of facts and then abstracts them into fact types.Constraints andrules ofrelationships andderivationgetadded tothemodel tomakeit complete.

Figure 1-20 shows an ORM diagram for doctor scheduling.Named ellipsesindicate entity types and have a method for referencing them.The reference (last name)shown inparentheseswithin the ellipse for Doctor means that doctors arereferred to by last names.The sample data form the fact instances,and these get abstracted into the fact types.The ORMdiagram indicates the structure consistingof the fact types of Doctor, Time,Patient,and PatientName. A named sequence of one or more role boxes depicts a relationship.In this case,we have a three-role or ternary relationship:Doctor at Time is scheduledfor Patient.Wealsohaveabinaryortwo-roleassociationbetweenPatient andPatientName.Themodeldiagram alsoincludessomecounterdata toindicate appropriate constraints.

An ORM diagram presents all factsin terms of entities or values.Unlike as inE-R,attributes arenot specifiedin thebase ORMmodels.Object-rolemodeling allowsforrelationshipswith multipleroles.Object-rolemodelingdiagrams tend tobelarge;nevertheless,an attribute-free model is simpler,more stable,and easier forvalidation.The arrow-tipped lines indicate uniqueness constraints showing whichroles or combination ofrolesmust

FIGURE1-20 ORMdiagram:doctorscheduling

<!-- image -->
