
<div class="chatbox">
  <div class="user-column">
    <p>
      Welcome back, {{username}}! {{err_msg}}
      <br>
      Select a friend to chat with:
    </p>

    <ul id="friend-list">
      % for i in range(0, len(friend_usernames)):
        <li>
          <a href="/chat/{{friend_ids[i]}}">{{friend_usernames[i]}}</a>
        </li>
      % end
    </ul>
  </div>

  <div class="add-friend-column">
    <h2>Add Friends</h2>

    % if add_msg:
    <div class="add-friend-entry">
      <p>{{!add_msg}}</p>
    </div>
    % end
  
    <div class="add-friend-entry">
      <p>Add a friend by their username</p>
      <form name="add-id-friend" action="/friends" method="post">
        <input name="username-input" autocomplete="off">
        <input type="hidden" name="add-type" value="add-username"/>
        <button type="submit">Add</button>
      </form>
    </div>

    <div class="add-friend-entry">
      <p>Find a random friend from one of your classes</p>
      <form name="add-class-friend" action="/friends" method="post">
        <input type="hidden" name="add-type" value="add-class"/>
        <button type="submit">Find</button>
      </form>
    </div>
  </div>
</div>
