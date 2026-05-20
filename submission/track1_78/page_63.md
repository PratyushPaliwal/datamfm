current year,broken down by regions,compared with prior year and targets,sorting the sales in ascending sequence by region?After viewing the sales data,suppose we want follow-upquestion such as:For theregion with the lowestperformance,what is thebreakdown by sales representatives,districts,and shipment methods.This approach of querying andanalysisislikelytoleadustothereasonsforthelowperformancesothatwecanmake strategic decisions torectify the situation.Therefore,a data warehouse must contain data extractedfrom OLTPsystems-data thatcanbeviewed andmodeled for queryingand analysis.

In this example,we want a data model that enables analysis of sales by year,region, sales representative,and shipment method.We needa model that supports analysis of sales data or facts about sales by combinations of the business dimensions of year, region,sales representative,and shipment method.The model should depict the information content in a datawarehouseusing dimensional modeling.Wewill discuss dimensional modeling technique in great detail in Chapter 9.That chapter describes data modelingfor decision-support systemsextensively.

## OtherModelingTrends

Some recent datamodeling and related trends include very-high-level languages for querying information systems,enhanced schema or model abstraction methods,newer sible markuplanguage (XML).In the remaining chapters,we will include discussions on these as and when necessary.

Letus now conclude withbrief discussions on a few other trends

PostrelationalDatabases.In ourearlier discussions,wehavenoted thatarelational data modelviews datain the form oftwo-dimensional tables.Wehavealso seen that a conceptual model may bemapped to a relationalmodel.Prior to the advent of the relationalmodelon the database scene,other models such as the hierarchical and network models preceded the relationalmodel.In these models,data is viewed differently.The hierarchicalmodelpresents data ashierarchical segments inparent-child relationships. On the other hand,the network model consists of data nodes arranged as a network. Still,a conceptualmodelwhilebeing transformed into a logicalmodelmay take any oneoftheseforms.

Therelational model isstill themostpopular andwidely usedmodel;most datasystem implementations are relational databases.However,the recent uses of data and thegenerationofnewer typesofdataposeproblemsfortherelationalmodel.Nowwehavetodeal with data intheform ofimages,sounds,and spatial elements.More complex data objects havebecomecommon inindustry.Arelationalmodel doesnot seemtobe adequatefor representing recent trends in data usage.Organizations adoptpostrelationalmodels to address therecentrequirements.Data modelersneed to adapt their modeling techniques toaccommodatepostrelationalmodels.

Let usbrieflyhighlight a few of thesepostrelational approaches.

Object-OrientedDatabases.Inaddition tofeatures ofrelational databases,these databasespossess additional featuressuch assupport for complex objects,encapsulation invol-
