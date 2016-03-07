A Static Blog Hosted In Company Network Shared Drive.

I am keeping a blog about my work in company. It serves as a venue for reflection and reference. It is only accessible from company network, as all the html files are kept in company's shared network folder.

First, this script creates the main.html. The script scan for new html files in blog directory and incrementally appends new content summary to the main page. If ever I want to generate the entire main page anew, just delete it and run the script again.

Html files are generated from org files in emacs. convert.el can convert org file to html file.

;; convert.el
(defun exportToHtml (path)
  (find-file path)
  (org-html-export-to-html)
  )
(exportToHtml "c:/blog/tg.org")
(exportToHtml "c:/blog/GoalFy15.org")
;; end convert.el
'''
