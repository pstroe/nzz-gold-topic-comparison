# nzz-gold-topic-comparison

project folder to get the most out of the work we have done to produce our ocr ground truth with nzz data. 

## annotation of categories

- the tool used for annotation is the vgg image annotator (http://www.robots.ox.ac.uk/~vgg/software/via/)
- annotation of categories done on the basis of http://show.newscodes.org/index.html?newscodes=subj&lang=en-GB&startTo=Show
- article boundaries are rectangles or polygons
- a horizontal line seperating articles always belongs to the article above
- the header is a separate "article", the line is included
- articles are assigned to one top category, but they can be assigned to several subcategories
