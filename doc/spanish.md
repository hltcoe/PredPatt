# es-dev-001-s255
> Live in the Navajo Nation es un DVD musical de la cantante canadiense Alanis Morissette , publicado el 27 de agosto de el año 2002 .

    ?a es un DVD musical de ?b
        ?a: Live in the Navajo Nation
        ?b: la cantante canadiense
    ?a is/are musical
        ?a: un DVD de la cantante canadiense
    ?a is/are canadiense
        ?a: la cantante
    ?a is/are Alanis Morissette
        ?a: la cantante canadiense
    ?a publicado ?b
        ?a: un DVD musical de la cantante canadiense
        ?b: el 27 de agosto de el año 2002

<!--parse=
nsubj(Live/0, DVD/7)              name(in/1, Live/0)
name(the/2, Live/0)               name(Navajo/3, Live/0)
name(Nation/4, Live/0)            cop(es/5, DVD/7)
det(un/6, DVD/7)                  root(DVD/7, ROOT/-1)
amod(musical/8, DVD/7)            case(de/9, cantante/11)
det(la/10, cantante/11)           nmod(cantante/11, DVD/7)
amod(canadiense/12, cantante/11)  appos(Alanis/13, cantante/11)
name(Morissette/14, Alanis/13)    punct(,/15, publicado/16)
acl(publicado/16, DVD/7)          det(el/17, 27/18)
nmod(27/18, publicado/16)         case(de/19, agosto/20)
nmod(agosto/20, 27/18)            case(de/21, año/23)
det(el/22, año/23)                nmod(año/23, agosto/20)
nummod(2002/24, año/23)           punct(./25, DVD/7)
-->
<!--tags=
Live/PROPN in/PROPN the/PROPN Navajo/PROPN Nation/PROPN es/VERB un/DET DVD/NOUN musical/ADJ de/ADP la/DET cantante/NOUN canadiense/ADJ Alanis/PROPN Morissette/PROPN ,/PUNCT publicado/VERB el/DET 27/NUM de/ADP agosto/PROPN de/ADP el/DET año/NOUN 2002/NUM ./PUNCT
-->

# es-dev-004-s62
> Después de los estudios de Roberval , Newton se percató de que el método de tangentes podía utilizar se para obtener las velocidades instantáneas de una trayectoria conocida .

After the studies of Roberval , Newton noticed that the method of tangents could be used to obtain instantaneous velocities of a known trajectory .

    Después de ?a ?b ?c percató
        ?a: los estudios de Roberval
        ?b: Newton
        ?c: se
    ?a ?b podía utilizar ?c
        ?a: Después los estudios de Roberval , percató
        ?b: el método de tangentes
        ?c: se
    ?a obtener ?b
        ?a: Newton
        ?b: las velocidades instantáneas de una trayectoria conocida
    ?a is/are instantáneas
        ?a: las velocidades de una trayectoria conocida
    ?a is/are conocida
        ?a: una trayectoria

<!--parse=
case(Después/0, estudios/3)   mwe(de/1, Después/0)           det(los/2, estudios/3)                nmod(estudios/3, percató/9)
case(de/4, Roberval/5)        nmod(Roberval/5, estudios/3)   punct(,/6, estudios/3)                nsubj(Newton/7, percató/9)
iobj(se/8, percató/9)         root(percató/9, ROOT/-1)       mark(de/10, utilizar/17)              mark(que/11, utilizar/17)
det(el/12, método/13)         nsubj(método/13, utilizar/17)  case(de/14, tangentes/15)             nmod(tangentes/15, método/13)
aux(podía/16, utilizar/17)    acl(utilizar/17, percató/9)    iobj(se/18, utilizar/17)              mark(para/19, obtener/20)
advcl(obtener/20, percató/9)  det(las/21, velocidades/22)    dobj(velocidades/22, obtener/20)      amod(instantáneas/23, velocidades/22)
case(de/24, trayectoria/26)   det(una/25, trayectoria/26)    nmod(trayectoria/26, velocidades/22)  amod(conocida/27, trayectoria/26)
punct(./28, percató/9)
-->

<!--tags=
Después/ADV de/ADP los/DET estudios/NOUN de/ADP Roberval/PROPN ,/PUNCT Newton/PROPN se/PRON percató/VERB de/ADP que/SCONJ el/DET método/NOUN de/ADP tangentes/NOUN podía/AUX utilizar/VERB se/PRON para/SCONJ obtener/VERB las/DET velocidades/NOUN instantáneas/ADJ de/ADP una/DET trayectoria/NOUN conocida/ADJ ./PUNCT
-->

The translation does pretty well though.
> After the studies of Roberval , Newton noticed that the method of tangents could be used to obtain instantaneous velocities of a known trajectory .

    After ?a , ?b noticed ?c
        ?a: the studies of Roberval
        ?b: Newton
        ?c: SOMETHING := the method of tangents could be used to obtain instantaneous velocities of a known trajectory
    ?a could be used to obtain ?b
        ?a: the method of tangents
        ?b: instantaneous velocities of a known trajectory
    ?a is/are instantaneous
        ?a: velocities of a known trajectory
