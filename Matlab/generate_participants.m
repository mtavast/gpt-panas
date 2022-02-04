%% Create participant descriptions
% 
% TODO:
% more gender categories

clc; clear all; close all;

rng(3)

nparticipants = 300;

age_r = linspace(24,60,37); % age of the participants
gender2_r = {'woman,', 'man,'};
% 50 jobs from https://hiring.monster.com/employer-resources/blog/job-trends/most-common-jobs-2016/
job_r = {'am a truck driver,', 
'am a registered nurse,',
'am a supervisor in a retail store,',
'am a retail salesperson,',
'am a software developer,',
'am a customer service representative,',
'am a marketing manager,',
'am a supervisor of food preparation and serving workers,',
'am a supervisor of office and administrative support workers,',
'am a computer user support specialist,',
'am a computer systems analyst,',
'am a network and computer systems administrator,',
'am a web developer,',
'am a management analyst,',
'am a medical and health services manager,',
'am an accountant,',
'am an information technology project manager,',
'am a sales manager,',
'am an industrial engineer,',
'am an executive secretaries assistant,',
'am a sales representative,',
'am a maintenance worker,',
'am a social and human service assistant,',
'am an entrepreneur,',
'am a supervisor of production and operating workers,',
'am a nursing assistant,',
'am a fast-food worker,',
'am a vocational nurse,',
'am a general manager,',
'am an auditing clerk,',
'am a manager,',
'am a financial manager,',
'am an insurance sales agent,',
'am a sales representative in wholesale and manufacturing,',
'am a sales agent in financial service,',
'am a critical care nurse,',
'am a cashier,',
'am a computer systems engineer,',
'am a market research analyst,',
'am a physical therapist,',
'am a medical assistant,',
'am a software quality assurance engineer,',
'am an information security analyst,',
'am a medical secretary,',
'am a freight laborer,',
'am a security guard,',
'am a family and general practitioner,'}

% https://www.notsoboringlife.com/popular-hobbies/
hobbies_r = {'I enjoy reading.',
'I watch TV.',
'I like to spend time with my family.',
'I like going to the movies.',
'I enjoy fishing.',
'I spend a lot of time on the computer.',
'I like gardening.',
'I watch a lot of movies.',
'I like to take walks.',
'I exercise a lot.',
'I enjoy listening to music.',
'I go on hunting trips.',
'I play many different team sports.',
'I enjoy shopping.',
'I like traveling.',
'I like socializing.',
'I enjoy sewing.',
'I play golf.',
'I spend a lot of time in church activities.',
'I like to relax.',
'I play music.',
'I spend a lot of time doing housework.',
'I enjoy crafts.',
'I watch a lot of sports.',
'I enjoy bicycling.',
'I like to play cards.',
'I enjoy hiking.',
'I like cooking.',
'I like to eat out.',
'I go on dates.',
'I enjoy swimming.',
'I go on camping trips.',
'I ski.',
'I like to fix cars.',
'I like writing.',
'I spend time on my boat.',
'I drive my motorcycle.',
'I take care of my pets.',
'I often go bowling.',
'I enjoy painting.',
'I enjoy running.',
'I like dancing.',
'I like horseback riding.',
'I play tennis.',
'I often go to the theatre.',
'I play billiards.',
'I like to go to the beach.',
'I do a lot of volunteer work.'}

text = cell(1);

for i = 1:nparticipants

    age = datasample(age_r, 1);
    gender = datasample(gender2_r, 1);
    job = datasample(job_r, 1);
    hobbies = datasample(hobbies_r, 1);
    
    text = (['Participant: I''m a' gender num2str(age) 'years old. I' job 'and in my free time,' hobbies]);
    c=cellfun(@string,text);
    participants(i,1) = join(c);
    
end

% Are there identical participants
for i=1:nparticipants
    for s=1:nparticipants
        if isequal(participants(i), participants(s))
            if i ~= s
              disp([num2str(i) num2str(s)])
            end
        end
    end
end

writematrix(participants, 'participants.csv')
