<?php
include 'global/config.php';
include 'carrito.php';
include 'templates/cabecera.php';
include 'templates/body.php';
?>

<br>
<!--
<div class="alert alert-success">
    <?php echo ($mensaje);?>
</div>
-->
<h3>Lista del Carrito</h3>

<?php if(!empty($_SESSION['CARRITO'])){?>

<table class="table table-light table-bordered">
    <tbody>
        <tr>
            <th width=40%>Descripción</th>
            <th width=15% class="text-center">Cantidad</th>
            <th width=20% class="text-center">Precio</th>
            <th width=20% class="text-center">Total</th>
            <th width=5%>--</th>
        </tr>

        <?php $total=0; ?>

        <?php foreach ($_SESSION['CARRITO'] as $indice => $producto) { ?>
        <tr>
            <td width=40%><?php echo $producto['NOMBRE']?></td>
            <td width=15% class="text-center"><?php echo $producto['CANTIDAD']?>
                <button class="btn btn-primary" 
                type="submit" 
                name="btnAccion" 
                value="mas">+</button>

                <button class="btn btn-primary" 
                type="submit" 
                name="btnAccion" 
                value="menos">-</button>
            </td>
            <td width=20% class="text-center">$<?php echo $producto['PRECIO']?></td>
            <td width=20% class="text-center">$<?php echo number_format($producto['PRECIO']*$producto['CANTIDAD'],2)?></td>

            <td width=5%>
                <form action="" method="post">
                    <input type="hidden" 
                    name="id" 
                    id="id" 
                    value="<?php echo openssl_encrypt($producto['ID'],COD,KEY); ?>">

                    <button class="btn btn-danger" 
                    type="submit" 
                    name="btnAccion" 
                    value="Eliminar"> Eliminar</button>

                </form>
            </td>
        </tr>
        <?php $total= $total+($producto['PRECIO']*$producto['CANTIDAD']); ?>
        <?php } ?>

        <tr>
            <td colspan="3" align="right"><h3>Total</h3></td>
            <td align="right"><h3>$<?php echo number_format($total,2); ?></h3></td>
            <td></td>
        </tr>
        
        <tr>
            <td colspan="5">
                <form action="" method="post" >
                    <div class="alert alert-success">
                        <div class="form-group">
                            <label for="my-input">Correo de contacto:</label>
                            <input id="id" name="id" class="form-control" type="email" placeholder="Por favor escribe tu correo" required>
                        </div>

                        <small id="emailHelp" class="form-text text-muted">
                            Los productos se enviarán a este correo.
                        </small>

                    </div>
                    <input type="hidden" 
                    name="id" 
                    id="id" 
                    value="<?php echo openssl_encrypt($producto['ID'],COD,KEY); ?>">

                    <div class="btn-group btn-group-toggle" data-toggle="buttons">
                        <label>
                            <input id="pago" name="tarjeta" type="radio">Pago con tarjeta&nbsp;
                            <input id="pago" name="paypal" type="radio">Pago con PayPal<br> <br>
                        </label>
                    </div> <br>

                    <button class="btn btn-primary btn-lg btn-block" type="submit" name="btnAccion" value="Proceder">Proceder a pagar >></button>
                    
                </form>

                

            </td>
        </tr>
        
    </tbody>
</table>
<a href="reportes.php"> <button class="btn btn-primary" type="submit">PDF</button> </a>

<?php }else{ ?>
    <div class="alert alert-success"> No hay productos en el carito... Agregue uno</div>
<?php } ?>

<?php include 'templates/pie.php' ?>