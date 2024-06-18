import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = { # 移動量辞書
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんrct, 爆弾rct
    戻り地：真理値タプル(横方向, 縦方向)
    画面内ならTrue, 画面内ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def game_over(screen: int) -> None:
    """
    ゲームオーバー画面
    画面をブラックアウトし，
    泣いているこうかとん画像"fig/3.png"と
    「Game Over」の文字列を
    5秒間表示させる関数を実装する
    """
    # 背景の描画
    rect = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    rect.set_alpha(200)
    pg.draw.rect(rect, (0, 0, 0, 128), (0, 0, WIDTH, HEIGHT))
    screen.blit(rect, (0, 0))
    #テキストの描画
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT //2)
    screen.blit(text, text_rect)
    # こうかとんの描画
    cry_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    cry_kk_rct = cry_kk_img.get_rect()
    cry_kk_rct.center = (WIDTH // 4, HEIGHT //2) # 左のこうかとん
    screen.blit(cry_kk_img, cry_kk_rct)
    cry_kk_rct.center = (WIDTH // 4 + WIDTH // 2, HEIGHT //2) #右のこうかとん
    screen.blit(cry_kk_img, cry_kk_rct)
    pg.display.update()
    pg.time.wait(5000) # 5秒停止


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20)) # 1辺が20の空のSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #からのSurfaceに赤い円を描く
    bb_rct = bb_img.get_rect()
    bb_rct.center =random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5 # 爆弾の横縦速度ベクトル
    bb_img.set_colorkey((0, 0, 0))
    clock = pg.time.Clock()
    tmr = 0


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        if kk_rct.colliderect(bb_rct):# 衝突判定
            game_over(screen)
            break
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
