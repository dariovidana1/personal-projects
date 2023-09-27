<?php
include 'global/config.php';
include 'global/conexion.php';
include 'carrito.php';
include 'templates/cabecera.php';

include 'templates/body.php';

include 'archivos/carrusel.html';


//script fondo
?>
        
        
        <br>
        
        <div class="row">
            <?php
                
                $sentencia=$pdo->prepare("SELECT * FROM `tblproductos`");
                $sentencia->execute();
                $listaProductos=$sentencia->fetchAll(PDO::FETCH_ASSOC);
                    
            ?>

            <?php foreach($listaProductos as $producto){ ?>
                
                <div class="col-3">
                <div class="card">
                    <img 
                    title="<?php echo $producto['DESCRIPCION']?>"
                    alt="Titulo"
                    class="card-img-top" 
                    src="<?php echo $producto['IMAGEN'];?>" 

                    data-toggle="popover"
                    data-trigger="hover"
                    data-content="<?php echo $producto['DESCRIPCION'];?>"
                    height="350"

                    >
                    <div class="card-body">
                        <span><?php echo $producto['NOMBRE'];?></span>
                        <h5 class="card-title">$<?php echo $producto['PRECIO'];?></h5>
                        <p class="card-text"><?php echo $producto['DESCRIPCION'];?></p>
                        <form action="" method="post">
                            <input type="hidden" name="id" id="id" value="<?php echo openssl_encrypt($producto['ID'],COD,KEY);?>">
                            <input type="hidden" name="nombre" id="nombre" value="<?php echo openssl_encrypt($producto['NOMBRE'],COD,KEY);?>">
                            <input type="hidden" name="precio" id="precio" value="<?php echo openssl_encrypt($producto['PRECIO'],COD,KEY);?>">
                            <input type="hidden" name="cantidad" id="cantidad" value="<?php echo openssl_encrypt(1,COD,KEY);?>">

                            <button class="btn btn-primary" name="btnAccion" value="Agregar" type="submit">Agregar al carrito</button>
                        </form>
                            
                    </div>
                </div>
            </div>

            <?php } ?>
                
        </div>
    </div>

    <script>
        
        $(function () {
            $('[data-toggle="popover"]').popover()
        })

    </script>
<?php include 'templates/pie.php' ?>
