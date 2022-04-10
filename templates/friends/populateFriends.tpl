    <p>
        Welcome back, {{username}}! {{err_msg}}
        <br>
        Select a friend to chat with:
    </p>
    

    
    <ul>
      % for i in range(0, len(friend_usernames)):
        <li>
          <a href="/chat/{{friend_ids[i]}}">{{friend_usernames[i]}}</a>
        </li>
      % end
    </ul>
</p>
