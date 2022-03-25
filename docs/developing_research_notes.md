# DCR - Developing - Research Notes

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.0)

----

## Papers

#### Hegghammer, T. (2021)
**OCR with Tesseract, Amazon Textract, and Google Document AI: a benchmarking experiment.**
Journal of Computational Social Science, 2021, pp. 2432-2725 [Online]
Available at [https://doi.org/10.1007/s42001-021-00149-1](https://doi.org/10.1007/s42001-021-00149-1){:target="_blank"}
(Accessed 04 January 2022).

Optical Character Recognition (OCR) can open up understudied historical documents to computational analysis, but the accuracy of OCR software varies.
This article reports a benchmarking experiment comparing the performance of Tesseract, Amazon Textract, and Google Document AI on images of English and Arabic text.
English-language book scans (n=322) and Arabic-language article scans (n=100) were replicated 43 times with different types of artificial noise for a corpus of 18,568 documents, generating 51,304 process requests.
Document AI delivered the best results, and the server-based processors (Textract and Document AI) performed substantially better than Tesseract, especially on noisy documents.
Accuracy for English was considerably higher than for Arabic.
Specifying the relative performance of three leading OCR products and the differential effects of commonly found noise types can help scholars identify better OCR solutions for their research needs.
The test materials have been preserved in the openly available “Noisy OCR Dataset” (NOD) for reuse in future benchmarking studies.

#### Minaee, S. et al. (2021)
**Deep Learning Based Text Classification: A Comprehensive Review.**
arXiv [Online]
Available at [https://arxiv.org/abs/2004.03705](https://arxiv.org/abs/2004.03705){:target="_blank"}
(Accessed 04 January 2022).

Deep learning based models have surpassed classical machine learning based approaches in various text classification tasks, including sentiment analysis, news categorization, question answering, and natural language inference. 
In this paper, we provide a comprehensive review of more than 150 deep learning based models for text classification developed in recent years, and discuss their technical contributions, similarities, and strengths. 
We also provide a summary of more than 40 popular datasets widely used for text classification. 
Finally, we provide a quantitative analysis of the performance of different deep learning models on popular benchmarks, and discuss future research directions.

#### Paaß G., Konya I. (2011)
**Machine Learning for Document Structure Recognition.** 
In: Mehler A., Kühnberger KU., Lobin H., Lüngen H., Storrer A., Witt A. (eds) Modeling, Learning, and Processing of Text Technological Data Structures. 
Studies in Computational Intelligence, vol 370. 
Springer Verlag GmbH, Heidelberg, Germany. 
Available at [https://www.researchgate.net/publication/265487498_Machine_Learning_for_Document_Structure_Recognition](https://www.researchgate.net/publication/265487498_Machine_Learning_for_Document_Structure_Recognition){:target="_blank"}
(Accessed 04 January 2022).

The backbone of the information age is digital information which may be searched, accessed, and transferred instantaneously. 
Therefore the digitization of paper documents is extremely interesting. 
This chapter describes approaches for document structure recognition detecting the hierarchy of physical components in images of documents, such as pages, paragraphs, and figures, and transforms this into a hierarchy of logical components, such as titles, authors, and sections. 
This structural information improves readability and is useful for indexing and retrieving information contained in documents. 
First we present a rule-based system segmenting the document image and estimating the logical role of these zones. 
It is extensively used for processing newspaper collections showing world-class performance. 
In the second part we introduce several machine learning approaches exploring large numbers of interrelated features. 
They can be adapted to geometrical models of the document structure, which may be set up as a linear sequence or a general graph. 
These advanced models require far more computational resources but show a better performance than simpler alternatives and might be used in future.

#### Power R., Scott D., Bouayad-Agha, N. (2003)
**Document Structure.**
Computational Linguistics, 2003, Volume 29, Issue 2, pp. 211-260 [Online]
The MIT Press, Cambridge, USA.
Available at [https://direct.mit.edu/coli/article/29/2/211/1803/Document-Structure](https://direct.mit.edu/coli/article/29/2/211/1803/Document-Structure){:target="_blank"}
(Accessed 05 January 2022).

We argue the case for abstract document structure as a separate descriptive level in the analysis and generation of written texts. 
The purpose of this representation is to mediate between the message of a text (i.e., its discourse structure) and its physical presentation (i.e., its organization into graphical constituents like sections, paragraphs, sentences, bulleted lists, figures, and footnotes). 
Abstract document structure can be seen as an extension of Nunberg's “text-grammar” it is also closely related to “logical” markup in languages like HTML and LaTEX. 
We show that by using this intermediate representation, several subtasks in language generation and language understanding can be defined more cleanly.

#### Rahman, M., Finin, T. (2019)
_Unfolding the Structure of a Document using Deep Learning._
arXiv [Online]
Available at [https://arxiv.org/abs/1910.03678](https://arxiv.org/abs/1910.03678){:target="_blank"}
(Accessed 07 January 2022).

Understanding and extracting of information from large documents, such as business opportunities, academic articles, medical documents and technical reports, poses challenges not present in short documents. 
Such large documents may be multi-themed, complex, noisy and cover diverse topics. 
We describe a framework that can analyze large documents and help people and computer systems locate desired information in them. 
We aim to automatically identify and classify different sections of documents and understand their purpose within the document. 
A key contribution of our research is modeling and extracting the logical and semantic structure of electronic documents using deep learning techniques. 
We evaluate the effectiveness and robustness of our framework through extensive experiments on two collections: more than one million scholarly articles from arXiv and a collection of requests for proposal documents from government sources. 

