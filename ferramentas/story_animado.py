"""Transforma uma arte (story.jpg 1080x1920) em Story ANIMADO de 7s com movimento e trilha original.
Efeitos: zoom lento (Ken Burns), flash de entrada, brilho passando, leve tremor no início.
Uso: python3 ferramentas/story_animado.py posts/<data>/<nome>/story.jpg posts/<data>/<nome>/story.mp4 [seed_musica]
"""
import os, sys, subprocess, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__))

def main():
    src, out = sys.argv[1], sys.argv[2]
    seed = sys.argv[3] if len(sys.argv) > 3 else '5'
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, 'm.wav')
    subprocess.run([sys.executable, os.path.join(AQUI, 'reels', 'musica.py'), wav, seed], check=True, stdout=subprocess.DEVNULL)
    D, FPS = 7, 30
    N = D * FPS
    vf = (
        f"scale=2160:3840,zoompan=z='if(lt(on,8),1.08-0.01*on,1.0+0.035*on/{N})':"
        f"x='iw/2-(iw/zoom/2)+if(lt(on,10),(10-on)*3*sin(on*2),0)':y='ih/2-(ih/zoom/2)':d={N}:s=1080x1920:fps={FPS},"
        # flash branco de entrada
        f"fade=t=in:st=0:d=0.35:color=white,"
        # brilho diagonal passando (0.8s a 1.8s)
        "geq=lum='lum(X,Y)+if(between(T,0.8,1.8),40*exp(-pow((X+Y*0.5-(T-0.8)*2600)/90,2)),0)':cb='cb(X,Y)':cr='cr(X,Y)',"
        f"fade=t=out:st={D-0.4}:d=0.4,format=yuv420p"
    )
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', src, '-ss', '3.87', '-i', wav,
                    '-vf', vf, '-t', str(D), '-map', '0:v', '-map', '1:a',
                    '-af', f'afade=t=in:d=0.2,afade=t=out:st={D-0.8}:d=0.8,volume=0.8',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-c:a', 'aac', '-b:a', '160k',
                    '-movflags', '+faststart', out], check=True)
    print(out)

if __name__ == '__main__':
    main()
