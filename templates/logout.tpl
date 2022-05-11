</center>

<div>
    <p>You have successfully logged out. Redirecting to login page in 5 seconds.</p>
</div>

<script>
    window.sessionStorage.clear();
    setTimeout(function() { window.location.replace("/login"); }, 5000);
</script>