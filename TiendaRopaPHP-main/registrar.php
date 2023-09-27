<?php

include '../tienda_php2/templates/cabecera.php';

include 'carrito.php';

/*
  $conn = connect();
  $message = '';

  if (!empty($_POST['CORREO']) && !empty($_POST['CONTRA'])) {
    $sql = "INSERT INTO tblregistro (CORREO, CONTRA) VALUES (:CORREO, :CONTRA)";
    $stmt = $conn->prepare($sql);
    $stmt->bindParam(':CORREO', $_POST['CORREO']);

    $password = password_hash($_POST['CONTRA'],PASSWORD_BCRYPT);
    $stmt->bindParam(':CONTRA', $password);

    if ($stmt->execute()) {
      $message = 'Usuario creado';
    } else {
      $message = 'Error al crear cuenta';
    }
  }*/
?>

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>REGÍSTRATE</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>
  </head>
  <body>

    <?php if(!empty($message)): ?>
      <p> <?= $message ?></p>
    <?php endif; ?>

    <h1 align=center>REGÍSTRATE o <a href="ingresar.php">INGRESA</a> </h1>

    <form action="" method="POST" align=center name="formLogin" onSubmit="return validar()">
      <input name="CORREO" type="text" placeholder="Enter your email"> <br>
      <input name="CONTRA" type="password" placeholder="Enter your Password"> <br>
      <button class="btn btn-primary" name="btnAccion" type="submit" value="Registro">Submit</button>
    </form>

    <script> 
      function validar(){
        if((document.formLogin.CORREO.value.length == 0) || (document.formLogin.CONTRA.value.length == 0)){
          alert('Atención: Campos vacíos.');
          return false;
        }
        
        var ercorreo=/^[^@]+@[^@]+\.[a-zA-Z]{2,}$/;

        if(!(ercorreo.test(document.formLogin.CORREO.value))){
          alert('Atención: Correo no autorizado.');
          return false;
        }

      

        return true;
      }
    </script>

<?php include 'templates/pie.php' ?>