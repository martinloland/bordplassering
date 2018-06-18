email_cols = [1,3,5,7,9,11,13,15,17,19]
normal_email_col = 3
normal_student_name_first_col = 2
normal_student_name_last_col = 1
normal_folge_col = [5,6]
extra_email_col = 3
extra_student_name_first_col = 1
extra_student_name_last_col = 2
extra_folge_col = 4

n_seated = 0

def registration_dict():
    d = {}
    with open('normal.csv', 'r') as f:
        for line in f:
            parts = line.rstrip().split(',')
            if parts[0]:
                email = parts[normal_email_col]
                name = '{} {}'.format(parts[normal_student_name_first_col],
                                      parts[normal_student_name_last_col])
                folge = []
                for col in normal_folge_col:
                    if parts[col]:
                        folge.append(parts[col])
                d.update({email:{'name':name.rstrip(),
                                 'folge':folge,
                                 'seated':False}})
    with open('ekstra.csv', 'r') as f:
        for line in f:
            parts = line.rstrip().split(',')
            if parts[0]:
                email = parts[extra_email_col]
                folge = parts[extra_folge_col].split(';')
                folge = [f.rstrip() for f in folge]
                if email in d:
                    d[email]['folge'].extend(folge)
                else:
                    print('Could not find {} in normal'.format(email))
    return d



def valid_line(line):
    parts = line.rstrip().split(',')
    if parts[0].isnumeric() and parts[1]:
        return True
    else:
        return False

def table_dict(line):
    parts = line.rstrip().split(',')
    table = int(parts[0])
    guests = []
    for column in email_cols:
        if parts[column]:
            if parts[column].startswith('Ansatte'):
                guests.append({'email':'ansatte',
                               'n_people':1})
            else:
                guests.append({'email':parts[column],
                               'n_people':int(parts[column+1])})
    d = {'table':table,
         'guests':guests}
    return d

def log(text):
    printer = False

    if printer:
        print(text)
    else:
        with open('output.txt', 'a') as out_file:
            out_file.write(text+'\n')

def clear_output():
    open('output.txt', 'w').close()

def seat_person(text):
    global n_seated
    log(text)
    n_seated = n_seated + 1

clear_output()
people = registration_dict()

with open('plassering.csv', 'r') as f:
    for line in f:
        if valid_line(line):
            d = table_dict(line)
            log('\nBord {}'.format(d['table']))
            total_bord_people = 0
            for student in d['guests']:

                email = student['email'].rstrip()
                reserved_spaces = student['n_people']
                if email in people:
                    seat_person('\t'+people[email]['name'])
                    total_bord_people = total_bord_people + 1
                    people[email].update({'seated':True})

                    for name in people[email]['folge']:
                        seat_person('\t'+name)
                        total_bord_people = total_bord_people + 1

                    if reserved_spaces is not len(people[email]['folge'])+1:
                        log('\t\tERROR ON RESERVED SPACES FOR {}: reserved={}, needs={}'
                            .format(email, reserved_spaces, len(people[email]['folge'])+1))

                elif email == 'ansatte':
                    log('\t'+'Ansatte')
                    n_seated = n_seated + 8
                    total_bord_people = 8
                else:
                    log('\t\tERROR ON FINDING PERSON {}'.format(email))

            # log('\n' * (25 - total_bord_people))
            print('Bord {:<3}:{:>3} personer'.format(d['table'],
                                                 total_bord_people))
    print('\nTotalt: {} personer'.format(n_seated))


log('\n{} people has been seated'.format(n_seated))

log('Has not been seated:')
for key in people:
    if not people[key]['seated']:
        log('\t{}'.format(key))