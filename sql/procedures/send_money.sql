create
or replace procedure send_money(
sender_id int,
friend_id int,
amount int
) language plpgsql as 
$$ 

begin 
update users
set
credit = credit - amount
where
users.id = sender_id;
update users
set
credit = credit + amount
where
users.id = friend_id;
 
commit;
end;
$$