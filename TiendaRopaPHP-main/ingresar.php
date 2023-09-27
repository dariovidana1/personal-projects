<?php
include("login/conexionL.php");

$conn = connect();

session_start();

if (!empty($_POST['CORREO']) && !empty($_POST['CONTRA'])) {
  $sql = "SELECT ID, CORREO, CONTRA FROM tblregistro WHERE CORREO = :CORREO";
  $records = $conn->prepare($sql);
  $records->bindParam(':CORREO', $_POST['CORREO']);
  $records->execute();
  $results = $records->fetch(PDO::FETCH_ASSOC);

  $message = '';

  if(!$results){
    $message = 'Correo no autorizado';
  }else{
    if (count($results) > 0 /*&& password_verify($_POST['CONTRA'], $results['CONTRA'])*/) {
      $_SESSION['user_id'] = $results['ID'];
      header('Location:index.php');
    } else {
      $message = 'Contraseña incorrecta';
    }
  }
  
}

?>

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>INICIAR SESIÓN</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>
  </head>
  <body>

    <?php if(!empty($message)): ?>
      <p> <?= $message ?></p>
    <?php endif; ?>

    <h1 align=center>INGRESA or <a href="registrar.php">REGÍSTRATE</a> </h1>

    <form method="POST" name="formLogin" onSubmit="return validar()" action="ingresar.php" align="center">
      <input name="CORREO" type="text" placeholder="Enter your email"> <br>
      <input name="CONTRA" type="password" placeholder="Enter your Password"> <br>
      <input type="submit" value="Submit">
    </form>

    <script> 
      function validar(){
        if((document.formLogin.CORREO.value.length == 0) || (document.formLogin.CONTRA.value.length == 0)){
          alert('Atención: Campos vacíos.');
          return false;
        }
        
        var ercorreo=/^[^@\s]+@[^@\s]+\.[^@\s]+$/;

        if(!(ercorreo.test(document.formLogin.CORREO.value))){
          alert('Atención: Correo no autorizado.');
          return false;
        }

        return true;
      }
    </script>
  </body>
</html>