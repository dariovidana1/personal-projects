<?php
    require '../tienda_php2/archivos/conexion.php';
    require '../tienda_php2/login/conexionL.php';

    session_start();
    $mensaje="";

    if(isset($_POST['btnAccion'])){
        switch($_POST['btnAccion']){
            case 'Agregar':
                //mensaje ID
                if(is_numeric(openssl_decrypt($_POST['id'],COD,KEY))){
                    $ID=openssl_decrypt($_POST['id'],COD,KEY);
                    //$mensaje.="Ok ID correcto ".$ID."</br>";
                }else{
                    //$mensaje.="Ups... ID incorrecto ".$ID."</br>"; break;
                }

                //mensaje NOMBRE
                if(is_string(openssl_decrypt($_POST['nombre'],COD,KEY))){
                    $NOMBRE=openssl_decrypt($_POST['nombre'],COD,KEY);
                    //$mensaje.="NOMBRE... Ok ".$NOMBRE."</br>";
                }else{
                    $mensaje.="Ups... algo ocurrió con el NOMBRE".$NOMBRE."</br>"; break;
                }

                //mensaje CANTIDAD
                if(is_numeric(openssl_decrypt($_POST['cantidad'],COD,KEY))){
                    $CANTIDAD=openssl_decrypt($_POST['cantidad'],COD,KEY);
                    //$mensaje.="CANTIDAD... Ok ".$CANTIDAD."</br>";
                }else{
                    $mensaje.="Ups... algo ocurrió con la CANTIDAD".$CANTIDAD."</br>"; break;
                }

                //mensaje PRECIO
                if(is_numeric(openssl_decrypt($_POST['precio'],COD,KEY))){
                    $PRECIO=openssl_decrypt($_POST['precio'],COD,KEY);
                    //$mensaje.="PRECIO... Ok $".$PRECIO."</br>";
                }else{
                    $mensaje.="Ups... algo ocurrió con el Nombre".$PRECIO."</br>"; break;
                }

                


                if(!isset($_SESSION['CARRITO'])){
                    
                    $producto=array(
                        'ID'=>$ID,
                        'NOMBRE'=>$NOMBRE,
                        'CANTIDAD'=>$CANTIDAD,
                        'PRECIO'=>$PRECIO
                    );
                    $_SESSION['CARRITO'][0]=$producto;
                   

                    $insert=$pdo->prepare("INSERT INTO `tblcompra` (`NOMBRE`, `PRECIO`, `CANTIDAD`) 
                                                            VALUES (:Nombre, :Precio, :Cantidad)");
                    $insert->bindParam(":Nombre", $producto['NOMBRE']);
                    $insert->bindParam(":Precio", $producto['PRECIO']);
                    $insert->bindParam(":Cantidad", $producto['CANTIDAD']);         
                    
                    $insert->execute();
                    


                } else {

                    $idProductos=array_column($_SESSION['CARRITO'],"ID");

                    if(in_array($ID,$idProductos)){
                        echo "<script>alert('El producto ya ha sido seleccionado...');</script>";
                        
                    }else{

                        $NumeroProductos=count($_SESSION['CARRITO']);

                        $producto=array(
                            'ID'=>$ID,
                            'NOMBRE'=>$NOMBRE,
                            'CANTIDAD'=>$CANTIDAD,
                            'PRECIO'=>$PRECIO
                        );

                        $_SESSION['CARRITO'][$NumeroProductos]=$producto;

                        $insert=$pdo->prepare("INSERT INTO `tblcompra` (`ID`, `NOMBRE`, `PRECIO`, `CANTIDAD`) 
                                                            VALUES (:ID, :Nombre, :Precio, :Cantidad)");
                        $insert->bindParam(":ID", $producto['ID']);
                        $insert->bindParam(":Nombre", $producto['NOMBRE']);
                        $insert->bindParam(":Precio", $producto['PRECIO']);
                        $insert->bindParam(":Cantidad", $producto['CANTIDAD']);

                        $insert->execute();
                    
                        $mensaje= "Producto agregado al carrito :D";
                    }

                    
                }

            break;

            case "Eliminar":
                $servidor="mysql:dbname=".BD.";host=".SERVIDOR;
                try{
                    $pdo= new PDO($servidor,USUARIO,PASSWORD,
                    array(PDO::MYSQL_ATTR_INIT_COMMAND=>"SET NAMES utf8") );
                    //echo "<script>alert('Conectado...')</script>";

                }catch(PDOException $e){
                    //echo "<script>alert('Error...')</script>";
                }

                if(is_numeric(openssl_decrypt($_POST['id'],COD,KEY))){
                    $ID=openssl_decrypt($_POST['id'],COD,KEY);
                    
                    
                    foreach ($_SESSION['CARRITO'] as $indice=>$producto) {
                        if($producto['ID']==$ID){
                            unset($_SESSION['CARRITO'][$indice]);
                            echo "<script>alert('Elemento borrado...')</script>";

                            $elim=$pdo->prepare("DELETE FROM `tblcompra` WHERE `ID` = '$ID'");
                            $elim->execute();
                        }
                        
                    }

                }else{
                    $mensaje.="Ups... ID incorrecto ".$ID."</br>";
                }
            break;

            case "Proceder":

                $conexion=conectar();
                
                $carritoids=array();

                foreach ($_SESSION['CARRITO'] as $indice => $productoids) {
                    array_push($carritoids, $productoids['ID']);
                }

                

                for ($i=0; $i < count($carritoids); $i++) { 
                    $update="UPDATE tblproductos SET CANTIDAD = 
                            CANTIDAD - (SELECT CANTIDAD FROM tblcompra WHERE ID = '$carritoids[$i]') WHERE ID = '$carritoids[$i]';";
                    $queryup=mysqli_query($conexion,$update);
                }
                
                $sql="DELETE from tblcompra;";
                $sql=mysqli_query($conexion, $sql);

                if(isset($_SESSION['user_id'])){
                    session_unset();
                    header('Location:index.php');
                }else{
                    session_unset();
                    session_destroy();
                    header('Location:index.php');
                }


            break;

            case "Registro":

               

                $conn = connect();
                $message = '';

                if (!empty($_POST['CORREO']) && !empty($_POST['CONTRA'])) {
                    $sql = "INSERT INTO tblregistro (CORREO, CONTRA) VALUES (:CORREO, :CONTRA)";
                    $stmt = $conn->prepare($sql);
                    $stmt->bindParam(':CORREO', $_POST['CORREO']);

                    
                    //$password = password_hash($_POST['CONTRA'],PASSWORD_BCRYPT);
                    $stmt->bindParam(':CONTRA', $_POST['CONTRA']);

                    if ($stmt->execute()) {
                    $message = 'Usuario creado';
                    } else {
                    $message = 'Error al crear cuenta';
                    }
                }

                header('Location:ingresar.php');

                
                
            break;

        }
    }
?>