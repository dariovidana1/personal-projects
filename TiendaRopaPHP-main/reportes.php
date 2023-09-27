<?php 
    ob_start();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DARED</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
</head>
<body>
<?php
include 'archivos/conexion3.php';

$sentenciaSQL = $conexion->prepare("SELECT * FROM tblcompra");
$sentenciaSQL->execute();
$compra=$sentenciaSQL->fetchAll(PDO::FETCH_ASSOC);

include 'carrito.php';
include 'global/config.php';
include 'global/conexion.php';
?>


<table class="table table-light table-bordered">
    <br>
    <br>
    <tbody>
        <tr>
            <th width=40%>Descripción</th>
            <th width=15% class="text-center">Cantidad</th>
            <th width=20% class="text-center">Precio</th>
            <th width=20% class="text-center">Subtotal</th>
        </tr>
        <?php $total=0; ?>
            <?php foreach($_SESSION['CARRITO'] as $indice=>$producto){?>
                <tr>
                        <td width=40%><?php echo $producto['NOMBRE']?></td>
                        <td width=15% class="text-center"><?php echo $producto['CANTIDAD']?></td>
                        <td width=20% class="text-center"><?php echo $producto['PRECIO']?></td>
                        <td width=20% class="text-center"><?php echo number_format($producto['PRECIO']*$producto['CANTIDAD'],2)?></td>
                        
                </tr>
                <?php $total= $total+($producto['PRECIO']*$producto['CANTIDAD']); ?>
            <?php } ?>
            
            <tr>
                <td colspan="3" align="right"><h3>Total</h3></td>
                <td align="right"><h3>$<?php echo number_format($total,2); ?></h3></td>
                <td></td>
            </tr>
    </table>
</body>
</html>

<?php 
    $html=ob_get_clean();
    //echo $html;

    require_once 'libreria/dompdf/autoload.inc.php';
    use Dompdf\Dompdf;
    $dompdf = new Dompdf();

    $dompdf->loadHtml($html);
    $dompdf->setPaper('letter');

    $dompdf->render();
    $dompdf->stream("archivo.pdf", array("Attachment"=>false));
?>