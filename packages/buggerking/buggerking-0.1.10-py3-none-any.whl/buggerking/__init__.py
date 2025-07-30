import sys
from ._debugpy.src import debugpy as vendored_debugpy

# 'debugpy' 라는 이름으로 buggerking._debugpy.src.debugpy 모듈을 sys.modules 에 등록
sys.modules['debugpy'] = vendored_debugpy

from ._decorators import debug_decorator

# vendored_debugpy에서 __all__을 가져오거나, buggerking 패키지에서 노출할 API를 직접 정의합니다.
# 예시: vendored_debugpy의 모든 public API를 buggerking에서도 노출
__all__ = []
# if hasattr(vendored_debugpy, '__all__'):
#     __all__.extend(vendored_debugpy.__all__)
#     for name in vendored_debugpy.__all__:
#         globals()[name] = getattr(vendored_debugpy, name)
# else:
#     # __all__이 없는 경우, dir()을 사용하여 public으로 보이는 이름들을 가져올 수 있으나,
#     # 명시적으로 관리하는 것이 좋습니다.
#     for name in dir(vendored_debugpy):
#         if not name.startswith('_'):
#             globals()[name] = getattr(vendored_debugpy, name)
#             __all__.append(name)

__all__.append('debug_decorator')

# 기존 _dbg 별칭은 유지하거나 제거할 수 있습니다.
# sys.modules를 통해 'debugpy'로 접근 가능하므로, _dbg가 반드시 필요하지 않을 수 있습니다.
# _dbg = vendored_debugpy

