# Team EMU Small Group project

## Team members
The members of the team are:
- Nicole Lehchevska
- Dariana Dorin
- Krishi Wali
- Meilai Ji
- Xiangyi Liu


## Project structure
The project is called `system`.  It currently consists of a single app `clubs`.

## Deployed version of the application
The deployed version of the application can be found at [URL](https://still-meadow-94402.herokuapp.com/).

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```


## Sources
The packages used by this application are specified in `requirements.txt`

*Declare are other sources here.*

## Reused Code

We have reused part of this code, provided by https://bootstrapmade.com/selecao-bootstrap-template/, licensed by   
 
  * Template Name: Selecao - v4.7.0
  * Template URL: https://bootstrapmade.com/selecao-bootstrap-template/
  * Author: BootstrapMade.com
  * License: https://bootstrapmade.com/license/

The code was reused in clubs/templates/partial/club_profile.html
and in static/style.css and static/vendor dir.

The lines reused are approximately 500.
