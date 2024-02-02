# Course_Proposal
Build Web đề xuất khoá học với machine learning
   +Cosin Similarity 
   + K-NN

HOW TO BUILD APP :
    Config pyenv :
        MACBOOK:
                 Set up Vitural Environment
                  - pyenv install 3.10. 7
                  - pyenv local 3.10.7
                  - pyenv exec python -m venv .venv
                Build FrameWork in Requirements.txt : 
                  -pip install -r requirements.txt
                  -pip install -U scikit-learn
                Migrate Db to Postgresql:
                  - source .venv/bin/activate
                  = flask db init
                  - flask db migrate -m "Initial Create"
                  - flask db upgrade
      Window:
              Set up Vitural Environment
                  - pyenv install 3.10. 7
                  - pyenv local 3.10.7
                  - python -m venv .venv
                Build FrameWork in Requirements.txt : 
                  -pip install -r requirements.txt
                  -pip install -U scikit-learn
                Migrate Db to Postgresql:
                  - .\venv\Scripts\activate
                  = flask db init
                  - flask db migrate -m "Initial Create"
                  - flask db upgrade
