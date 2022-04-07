    <p>
        Welcome back, {{username}}! Select a friend to chat with:
    </p>
    

    
    <ul>
      %for friend in friend_usernames:
        <li>
          <a href="">{{friend}}</a>
        </li>
      %end
    </ul>
</p>
