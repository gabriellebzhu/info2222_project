<div>
    <p>You have successfully logged out. Redirecting to login page in 3 seconds.</p>
</div>

<script>
    window.sessionStorage.clear();
    setTimeout(function() { window.location.replace("/login"); }, 3000);
</script>