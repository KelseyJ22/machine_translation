A comment on the language F that you chose. You should make a brief statement of particular challenges in translating your choice of F language to English (relative to other possible choices for F), and key insights about the language that you made use of in your strategies to improve your baseline MT system.
Your corpus of 15 sentences, with clear indication of the dev-test split.
For each pre- or post-processing strategy you implement, a description of what differences between Language F and English that strategy was designed to address. Make sure you motivate the strategies by pointing to the characteristics of the dev set that led you to design them.
The output of Google Translate.
A comparative analysis commenting on your system's performance compared to Google Translate's. Show where the systems agree, what your system does better than Google Translate, and what Google Translate does better than your system.

It's very important to write a good report, since everyone will be writing different systems for different languages, so the TAs will not know much a priori about what you did. The grading will largely be based on your report and it is your job to clearly explain your efforts. You should explain your strategies and comment on your errors clearly and concisely, with examples.


Language Choice:
We chose to translate between Spanish and English because one of our team meembers is essentially fluent (although not a native speaker) and the others have at least a passing familiarity with the language. Spanish is similar to English in that there are many words similar in structure and the same alphabet is used, but both of these string similarities benefit human translators far more than machine translation systems, since they make it easier to remember Spanish words for an English speaker. Since remembering words is not an issue for computers, this is a minor aid. Spanish translation is complicated by the fact that word order is different than that of English (which is much more strictly SVO as compared to Spanish's lax ordering). While both are technically SVO languages, there are codified differences, such as that adjectives typically follow the noun they describe rather than preceding the verb as in English. Spanish also has a lot of small helper words that have little individual meaning outside of their context, for example "a" and "le" in A ella le gusta" (she likes); English largely lacks similar words. The final difficulty with Spanish-to-English translation lies in its use of accents and ñ, which we lack in English. Fortunately, this only complicates the use of simple ASCII characters, but doesn't add to the complexity of any translation we used algorithms. We could take advantage of the adjective-noun order pattern to improve sentence fluency by reordering these words; more general lack of concrete word order is harder to rectify in the less-flexible English.


Our Corpus:
Según los autores del estudio, estos dientes están compuestos de un material que es incluso más fuerte que la tela de araña.
Estos dientes se componen de fibras muy pequeñas, acomodadas de una manera particular.
Deberíamos pensar en hacer nuestras propias estructuras siguiendo los mismos principios de diseño.
Una niña de siete años aficionada a la tecnología necesita poco más de diez minutos para hackear una red inhalámbrica o wifipública.
Es lo que descubrió una empresa especializada en seguridad informática que quiso alertar sobre los peligros de conectarse a redes wifi sin la seguridad suficiente.
Betsy Davis es una niña de siete años que vive en Londres y a la que le gusta la tecnología.
Algunos no requieren un nombre de usuario y contraseña, por lo que están abiertos a cualquiera.
El Parlamento europeo tuvo que desconectar el año pasado su sistema de wifi público tras ser objeto de uno de estos ataques.
Al incorporar hilo de araña en la membrana, se mejoran enormemente sus propiedades conductoras.
En el caso de una batería, extiende su vida útil y el tiempo de funcionamiento antes de la próxima recarga.
Otra ventaja es que es un material natural. En términos ambientales, reduce el uso de elementos contaminantes utilizados comúnmente en las pilas.
El interés científico ha estado enfocado principalmente en cómo reproducir sus propiedades en un material sintético.
De acuerdo a la investigación, la banda infectó con malware o código maligno las computadoras de los empleados de las instituciones bancarias.
Se trata de un robo cibernético muy hábil y profesional.
Están tomando las medidas adecuadas para prevenir y detectar este tipo de ataques y minimizar cualquier efecto de estos sobre sus clientes.

Strategies:
1. Part of speech tagging in Spanish to choose appropriate English translation
2. Part of speech tagging in English to reorder adjectives and nouns
3. Eliminate duplicates in English sentences (usually "to")
4. NaiveBayes sentence probability to choose best translation from among options
5. NaiveBayes to test removal of words (because Spanish uses more words than English)
6. Address prepositions: "por"-->"by","of","from"; "que"-->"that","what"
7. Bidirectional NaiveBayes to fix things like "web" before "spider"
8. Idiomatic expression translation ("a ella le gusta"-->"she likes" rather than "to she it it pleases" as the dictionary would otherwise translate it)
9. 