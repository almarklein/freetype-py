# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
'''
FreeType high-level python API 

This the bindings for the high-level API of FreeType (that must be installed
somewhere on your system).

Note:
-----
C Library will be searched using the ctypes.util.find_library. However, this
search might fail. In such a case (or for other reasons), you can specify the
FT_library_filename before importing the freetype library and freetype will use
the specified one. 
'''
from ctypes import *
from ft_types import *
from ft_enums import *
from ft_errors import *
from ft_structs import *
import ctypes.util


FT_Library_filename = ctypes.util.find_library('freetype')
if not FT_Library_filename:
    raise RuntimeError, 'Freetype library not found'
__dll__ = ctypes.CDLL(FT_Library_filename)
__handle__ = None


# -----------------------------------------------------------------------------
# High-level API of FreeType 2
# -----------------------------------------------------------------------------
FT_Init_FreeType       = __dll__.FT_Init_FreeType
FT_Done_FreeType       = __dll__.FT_Done_FreeType
FT_Library_Version     = __dll__.FT_Library_Version
FT_Library_SetLcdFilter= __dll__.FT_Library_SetLcdFilter
FT_Library_SetLcdFilterWeights = __dll__.FT_Library_SetLcdFilterWeights
FT_New_Face            = __dll__.FT_New_Face
FT_New_Memory_Face     = __dll__.FT_New_Memory_Face
FT_Open_Face           = __dll__.FT_Open_Face
FT_Attach_File         = __dll__.FT_Attach_File
FT_Attach_Stream       = __dll__.FT_Attach_Stream
FT_Reference_Face      = __dll__.FT_Reference_Face
FT_Done_Face           = __dll__.FT_Done_Face
FT_Done_Glyph          = __dll__.FT_Done_Glyph
FT_Select_Size         = __dll__.FT_Select_Size
FT_Request_Size        = __dll__.FT_Request_Size
FT_Set_Char_Size       = __dll__.FT_Set_Char_Size
FT_Set_Pixel_Sizes     = __dll__.FT_Set_Pixel_Sizes
FT_Load_Glyph          = __dll__.FT_Load_Glyph
FT_Load_Char           = __dll__.FT_Load_Char
FT_Set_Transform       = __dll__.FT_Set_Transform
FT_Render_Glyph        = __dll__.FT_Render_Glyph
FT_Get_Kerning         = __dll__.FT_Get_Kerning
FT_Get_Track_Kerning   = __dll__.FT_Get_Track_Kerning
FT_Get_Glyph_Name      = __dll__.FT_Get_Glyph_Name
FT_Get_Glyph           = __dll__.FT_Get_Glyph
FT_Get_Postscript_Name = __dll__.FT_Get_Postscript_Name
FT_Get_Postscript_Name.restype = c_char_p
FT_Select_Charmap      = __dll__.FT_Select_Charmap
FT_Set_Charmap         = __dll__.FT_Set_Charmap
FT_Get_Charmap_Index   = __dll__.FT_Get_Charmap_Index
FT_Get_CMap_Language_ID= __dll__.FT_Get_CMap_Language_ID
FT_Get_CMap_Format     = __dll__.FT_Get_CMap_Format
FT_Get_Char_Index      = __dll__.FT_Get_Char_Index
FT_Get_First_Char      = __dll__.FT_Get_First_Char
FT_Get_Next_Char       = __dll__.FT_Get_Next_Char
FT_Get_Name_Index      = __dll__.FT_Get_Name_Index
FT_Get_SubGlyph_Info   = __dll__.FT_Get_SubGlyph_Info
FT_Get_FSType_Flags    = __dll__.FT_Get_FSType_Flags
FT_Get_Sfnt_Name_Count = __dll__.FT_Get_Sfnt_Name_Count
FT_Get_Sfnt_Name       = __dll__.FT_Get_Sfnt_Name

FT_Outline_GetInsideBorder  = __dll__.FT_Outline_GetInsideBorder
FT_Outline_GetOutsideBorder = __dll__.FT_Outline_GetOutsideBorder
FT_Stroker_New              = __dll__.FT_Stroker_New
FT_Stroker_Set              = __dll__.FT_Stroker_Set
FT_Stroker_Rewind           = __dll__.FT_Stroker_Rewind
FT_Stroker_ParseOutline     = __dll__.FT_Stroker_ParseOutline
FT_Stroker_BeginSubPath     = __dll__.FT_Stroker_BeginSubPath
FT_Stroker_EndSubPath       = __dll__.FT_Stroker_EndSubPath
FT_Stroker_LineTo           = __dll__.FT_Stroker_LineTo
FT_Stroker_ConicTo          = __dll__.FT_Stroker_ConicTo
FT_Stroker_CubicTo          = __dll__.FT_Stroker_CubicTo
FT_Stroker_GetBorderCounts  = __dll__.FT_Stroker_GetBorderCounts
FT_Stroker_ExportBorder     = __dll__.FT_Stroker_ExportBorder
FT_Stroker_GetCounts        = __dll__.FT_Stroker_GetCounts
FT_Stroker_Export           = __dll__.FT_Stroker_Export
FT_Stroker_Done             = __dll__.FT_Stroker_Done
FT_Glyph_Stroke             = __dll__.FT_Glyph_Stroke
FT_Glyph_StrokeBorder       = __dll__.FT_Glyph_StrokeBorder
FT_Glyph_To_Bitmap          = __dll__.FT_Glyph_To_Bitmap

# -----------------------------------------------------------------------------
# High-level python API 
# -----------------------------------------------------------------------------
def __del_library__(self):
    global __handle__
    if __handle__:
        try:
            FT_Done_FreeType(byref(self))
            __handle__ = None
        except:
            pass
FT_Library.__del__ = __del_library__


def get_handle():
    '''
    Get unique FT_Library handle
    '''
    global __handle__
    if not __handle__:
        __handle__ = FT_Library( )
        error = FT_Init_FreeType( byref(__handle__) )
        if error: raise FT_Exception(error)
        try:
            set_lcd_filter( FT_LCD_FILTER_DEFAULT )
        except:
            pass
        if error: raise FT_Exception(error)
    return __handle__



# -----------------------------------------------------------------------------
#  Stand alone functions
# -----------------------------------------------------------------------------
def version():
    '''
    Return the version of the FreeType library being used as a tuple of
    ( major version number, minor version number, patch version number )
    '''
    amajor = FT_Int()
    aminor = FT_Int()
    apatch = FT_Int()
    library = get_handle()
    FT_Library_Version(library, byref(amajor), byref(aminor), byref(apatch))
    return (amajor.value, aminor.value, apatch.value)


def set_lcd_filter(filt):
    '''
    This function is used to apply color filtering to LCD decimated bitmaps,
    like the ones used when calling FT_Render_Glyph with FT_RENDER_MODE_LCD or
    FT_RENDER_MODE_LCD_V.

    Note:
    -----

    This feature is always disabled by default. Clients must make an explicit
    call to this function with a 'filter' value other than FT_LCD_FILTER_NONE
    in order to enable it.

    Due to PATENTS covering subpixel rendering, this function doesn't do
    anything except returning 'FT_Err_Unimplemented_Feature' if the
    configuration macro FT_CONFIG_OPTION_SUBPIXEL_RENDERING is not defined in
    your build of the library, which should correspond to all default builds of
    FreeType.

    The filter affects glyph bitmaps rendered through FT_Render_Glyph,
    FT_Outline_Get_Bitmap, FT_Load_Glyph, and FT_Load_Char.

    It does not affect the output of FT_Outline_Render and
    FT_Outline_Get_Bitmap.

    If this feature is activated, the dimensions of LCD glyph bitmaps are
    either larger or taller than the dimensions of the corresponding outline
    with regards to the pixel grid. For example, for FT_RENDER_MODE_LCD, the
    filter adds up to 3 pixels to the left, and up to 3 pixels to the right.

    The bitmap offset values are adjusted correctly, so clients shouldn't need
    to modify their layout and glyph positioning code when enabling the filter.
    '''
    library = get_handle()
    error = FT_Library_SetLcdFilter(library, filt)
    if error: raise FT_Exception(error)



def set_lcd_filter_weights(a,b,c,d,e):
    '''
    Use this function to override the filter weights selected by
    FT_Library_SetLcdFilter. By default, FreeType uses the quintuple (0x00,
    0x55, 0x56, 0x55, 0x00) for FT_LCD_FILTER_LIGHT, and (0x10, 0x40, 0x70,
    0x40, 0x10) for FT_LCD_FILTER_DEFAULT and FT_LCD_FILTER_LEGACY.
    '''
    library = get_handle()
    weights = FT_Char(5)(a,b,c,d,e)
    error = FT_Library_SetLcdFilterWeights(library, weights)
    if error: raise FT_Exception(error)



# -----------------------------------------------------------------------------
#  Direct wrapper (simple renaming)
# -----------------------------------------------------------------------------
Vector = FT_Vector
Matrix = FT_Matrix

# -----------------------------------------------------------------------------
#  FT_BBox wrapper
# -----------------------------------------------------------------------------
class BBox( object ):
    def __init__(self, bbox):
        self._FT_BBox = bbox
    xMin = property(lambda self: self._FT_BBox.xMin)
    yMin = property(lambda self: self._FT_BBox.yMin)
    xMax = property(lambda self: self._FT_BBox.xMax)
    yMax = property(lambda self: self._FT_BBox.yMax)



# -----------------------------------------------------------------------------
#  FT_Size_Metrics wrapper
# -----------------------------------------------------------------------------
class SizeMetrics( object ):
    def __init__(self, metrics ):
        self._FT_Size_Metrics = metrics
    x_ppem = property( lambda self: self._FT_Size_Metrics.x_ppem )
    y_ppem = property( lambda self: self._FT_Size_Metrics.y_ppem )
    x_scale = property( lambda self: self._FT_Size_Metrics.x_scale )
    y_scale = property( lambda self: self._FT_Size_Metrics.y_scale )
    ascender = property( lambda self: self._FT_Size_Metrics.ascender )
    descender = property( lambda self: self._FT_Size_Metrics.descender )
    height = property( lambda self: self._FT_Size_Metrics.height )
    max_advance = property(lambda self: self._FT_Size_Metrics.max_advance )



# -----------------------------------------------------------------------------
#  FT_Bitmap_Size wrapper
# -----------------------------------------------------------------------------
class BitmapSize( object ):
    def __init__(self, size ):
        self._FT_Bitmap_Size = size
    x_ppem = property( lambda self: self._FT_Bitmap_Size.x_ppem )
    y_ppem = property( lambda self: self._FT_Bitmap_Size.y_ppem )
    size   = property( lambda self: self._FT_Bitmap_Size.size )
    height = property( lambda self: self._FT_Bitmap_Size.height )
    width  = property( lambda self: self._FT_Bitmap_Size.width )




# -----------------------------------------------------------------------------
#  FT_Bitmap wrapper
# -----------------------------------------------------------------------------
class Bitmap(object):
    def __init__(self, bitmap):
        self._FT_Bitmap = bitmap
    rows       = property(lambda self: self._FT_Bitmap.rows)
    width      = property(lambda self: self._FT_Bitmap.width)
    pitch      = property(lambda self: self._FT_Bitmap.pitch)
    num_grays  = property(lambda self: self._FT_Bitmap.num_grays)
    pixel_mode = property(lambda self: self._FT_Bitmap.pixel_mode)
    # palette_mode = property(lambda self: self._FT_Bitmap.palette_mode)
    # palette      = property(lambda self: self._FT_Bitmap.palette)
    def _get_buffer(self):
        data = [self._FT_Bitmap.buffer[i] for i in range(self.rows*self.pitch)]
        return data
    buffer     = property(_get_buffer)



# -----------------------------------------------------------------------------
#  FT_Charmap wrapper
# -----------------------------------------------------------------------------
class Charmap( object ):
    def __init__( self, charmap ):
        self._FT_Charmap = charmap
    encoding    = property( lambda self: self._FT_Charmap.contents.encoding)
    platform_id = property( lambda self: self._FT_Charmap.contents.platform_id)
    encoding_id = property( lambda self: self._FT_Charmap.contents.encoding_id)
    def _get_encoding_name(self):
        encoding = self.encoding
        for key,value in FT_ENCODINGS.items():
            if encoding == value:
                return key
        return 'Unknown encoding'
    encoding_name = property( _get_encoding_name )
    def _get_index( self ):
        return FT_Get_Charmap_Index( self._FT_Charmap )
    index = property( _get_index )
    def _get_cmap_language_id( self ):
        return FT_Get_CMap_Language_ID( self._FT_Charmap )
    cmap_language_id = property( _get_cmap_language_id )
    def _get_cmap_format( self ):
        return FT_Get_CMap_Format( self._FT_Charmap )
    cmap_format = property( _get_cmap_format )


# -----------------------------------------------------------------------------
#  FT_Outline wrapper
# -----------------------------------------------------------------------------
class Outline( object ):
    def __init__( self, outline ):
        self._FT_Outline = outline
        
    n_contours = property(lambda self: self._FT_Outline.n_contours)
    def _get_contours(self):
        n = self._FT_Outline.n_contours
        data = [self._FT_Outline.contours[i] for i in range(n)]
        return data
    contours = property(_get_contours)

    n_points = property(lambda self: self._FT_Outline.n_points)
    def _get_points(self):
        n = self._FT_Outline.n_points
        data = []
        for i in range(n):
            v = self._FT_Outline.points[i]
            data.append( (v.x,v.y) )
        return data
    points = property( _get_points )

    def _get_tags(self):
        n = self._FT_Outline.n_points
        data = [self._FT_Outline.tags[i] for i in range(n)]
        return data
    tags = property(_get_tags)
        
    flags = property(lambda self: self._FT_Outline.flags)


    def get_inside_border( self ):
        '''
        Retrieve the FT_StrokerBorder value corresponding to the 'inside'
        borders of a given outline.

        Return:
        The border index. FT_STROKER_BORDER_RIGHT for empty or invalid
        outlines.
        '''
        return FT_Outline_GetInsideBorder( self._FT_Outline )

    def get_outside_border( self ):
        '''
        Retrieve the FT_StrokerBorder value corresponding to the 'outside'
        borders of a given outline.

        Return:
        The border index. FT_STROKER_BORDER_RIGHT for empty or invalid
        outlines.
        '''
        return FT_Outline_GetInsideBorder( self._FT_Outline )



# -----------------------------------------------------------------------------
#  FT_Glyph wrapper
# -----------------------------------------------------------------------------
class Glyph( object ):
    '''
    The root glyph structure contains a given glyph image plus its advance
    width in 16.16 fixed float format.
    '''
    def __init__( self, glyph ):
        '''
        Create Glyph object from an FT glyph.

        Parameters:
        -----------
          glyph: valid FT_Glyph object
        '''
        self._FT_Glyph = glyph

    def __del__( self ):
        '''
        Destroy glyph.
        '''
        FT_Done_Glyph( self._FT_Glyph )

    def _get_format( self ):
        return self._FT_Glyph.contents.format
    format = property( _get_format )


    def stroke( self, stroker, destroy=False ):
        '''
        Stroke a given outline glyph object with a given stroker.

        Parameters:
        -----------
          stroker: A stroker handle.

          destroy: A Boolean. If 1, the source glyph object is destroyed on
                   success.
        Note:
        -----

        The source glyph is untouched in case of error.
        '''
        error = FT_Glyph_Stroke( byref(self._FT_Glyph),
                                 stroker._FT_Stroker, destroy )
        if error: raise FT_Exception( error )

    def to_bitmap( self, mode, origin, destroy=False ):
        '''
        Convert a given glyph object to a bitmap glyph object.

        Parameters:
        -----------
          mode: An enumeration that describes how the data is rendered.

          origin: A pointer to a vector used to translate the glyph image
                  before rendering. Can be 0 (if no translation). The origin is
                  expressed in 26.6 pixels.

          destroy: A boolean that indicates that the original glyph image
                   should be destroyed by this function. It is never destroyed
                   in case of error.

          Note:
          -----
            This function does nothing if the glyph format isn't scalable.

            The glyph image is translated with the ‘origin’ vector before
            rendering.

            The first parameter is a pointer to an FT_Glyph handle, that will
            be replaced by this function (with newly allocated
            data). Typically, you would use (omitting error handling):
        '''
        error = FT_Glyph_To_Bitmap( byref(self._FT_Glyph),
                                    mode, origin, destroy)
        if error: raise FT_Exception( error )
        return BitmapGlyph( self._FT_Glyph )


# -----------------------------------------------------------------------------
#  FT_BitmapGlyph wrapper
# -----------------------------------------------------------------------------
class BitmapGlyph( object ):
    '''
    A structure used for bitmap glyph images. This really is a 'sub-class' of
    FT_GlyphRec.
    '''
    def __init__( self, glyph ):
        '''
        Create Glyph object from an FT glyph.

        Parameters:
        -----------
          glyph: valid FT_Glyph object
        '''
        self._FT_BitmapGlyph = cast(glyph, FT_BitmapGlyph)

#    def __del__( self ):
#        '''
#        Destroy glyph.
#        '''
#        FT_Done_Glyph( FT_Glyph(self._FT_BitmapGlyph) )

    def _get_format( self ):
        return self._FT_BitmapGlyph.contents.format
    format = property( _get_format )

    def _get_bitmap( self ):
        return Bitmap( self._FT_BitmapGlyph.contents.bitmap )
    bitmap = property( _get_bitmap )

    def _get_left( self ):
        return self._FT_BitmapGlyph.left.value
    left = property( _get_left )

    def _get_top( self ):
        return self._FT_BitmapGlyph.top.value
    top = property( _get_top )


# -----------------------------------------------------------------------------
#  FT_GlyphSlot wrapper
# -----------------------------------------------------------------------------
class GlyphSlot( object ):
    def __init__( self, slot ):
        self._FT_GlyphSlot = slot

    def get_glyph( self ):
        aglyph = FT_Glyph()
        error = FT_Get_Glyph( self._FT_GlyphSlot, byref(aglyph) )
        if error: raise FT_Exception( error )
        return Glyph( aglyph )

    def _get_bitmap( self ):
        return Bitmap( self._FT_GlyphSlot.contents.bitmap )
    bitmap = property( _get_bitmap )

    def _get_next( self ):
        return GlyphSlot( self._FT_GlyphSlot.contents.next )
    next = property( _get_next )

    advance = property( lambda self: self._FT_GlyphSlot.contents.advance)

    def _get_outline( self ):
        return Outline( self._FT_GlyphSlot.contents.outline )
    outline = property( _get_outline )

    format  = property( lambda self:
                            self._FT_GlyphSlot.contents.format )
    bitmap_top  = property( lambda self:
                                self._FT_GlyphSlot.contents.bitmap_top )
    bitmap_left = property( lambda self:
                                self._FT_GlyphSlot.contents.bitmap_left )
    linearHoriAdvance = property( lambda self:
                                      self._FT_GlyphSlot.contents.linearHoriAdvance )
    linearVertAdvance = property( lambda self:
                                      self._FT_GlyphSlot.contents.linearVertAdvance )



# -----------------------------------------------------------------------------
#  Face wrapper
# -----------------------------------------------------------------------------
class Face( object ):
    
    def __init__( self, filename, index = 0 ):
        library = get_handle( )
        face = FT_Face( )
        error = FT_New_Face( library, filename, 0, byref(face) )
        if error: raise FT_Exception( error )
        self._filename = filename
        self._index = index
        self._FT_Face = face
    
    def set_char_size( self, width=0, height=0, hres=72, vres=72 ):
        error = FT_Set_Char_Size( self._FT_Face, width, height, hres, vres )
        if error: raise FT_Exception( error)

    def set_pixel_sizes( self, width, height ):
        error = FT_Set_Pixel_Sizes( self._FT_Face, width, height )
        if error: raise FT_Exception(error)

    def select_charmap( self, encoding ):
        error = FT_Select_Charmap( self._FT_Face, encoding )
        if error: raise FT_Exception(error)

    def set_charmap( self, charmap ):
        error = FT_Set_Charmap( self._FT_Face, charmap._FT_Charmap )
        if error : raise FT_Exception(error)

    def get_char_index( self, charcode ):
        if type( charcode ) is str:
            charcode = ord( charcode )
        return FT_Get_Char_Index( self._FT_Face, charcode )

    def get_first_char( self ):
        agindex = FT_UInt()
        charcode = FT_Get_First_Char( self._FT_Face, byref(agindex) )
        return charcode, agindex.value

    def get_next_char( self, charcode, agindex ):
        agindex = FT_UInt( agindex )
        charcode = FT_Get_Next_Char( self._FT_Face, charcode, byref(agindex) )
        return charcode, agindex.value

    def get_name_index( self, name ):
        return FT_Get_Name_Index( self._FT_Face, name )

    def set_transform( self, matrix, delta ):
        FT_Set_Transform( self._FT_Face,
                          byref(matrix), byref(delta) )

    def select_size( self, strike_index ):
        error = FT_Select_Size( self._FT_Face, strike_index )
        if error: raise FT_Exception( error )

    def load_glyph( self, index, flags = FT_LOAD_RENDER ):
        error = FT_Load_Glyph( self._FT_Face, index, flags )
        if error: raise FT_Exception( error )

    def load_char( self, char, flags = FT_LOAD_RENDER ):
        error = FT_Load_Char( self._FT_Face, ord(char), flags )
        if error: raise FT_Exception( error )

    def get_kerning( self, left, right, mode = FT_KERNING_DEFAULT ):
        left_glyph = self.get_char_index( left )
        right_glyph = self.get_char_index( right )
        kerning = FT_Vector(0,0)
        error = FT_Get_Kerning( self._FT_Face,
                                left_glyph, right_glyph, mode, byref(kerning) )
        if error: raise FT_Exception( error )
        return kerning

    def _get_sfnt_name_count(self):
        return FT_Get_Sfnt_Name_Count( self._FT_Face )
    sfnt_name_count = property(_get_sfnt_name_count)

    def get_sfnt_name( self, index ):
        '''
        Retrieve a string of the SFNT 'name' table for a given index
        '''
        name = FT_SfntName( )
        error = FT_Get_Sfnt_Name( self._FT_Face, index, byref(name) )
        if error: raise FT_Exception( error )
        return SfntName( name )

    def _get_postscript_name( self ):
        return FT_Get_Postscript_Name( self._FT_Face )
    postscript_name = property( _get_postscript_name )

    def _has_horizontal( self ):
        return bool( self.face_flags & FT_FACE_FLAG_HORIZONTAL )
    has_horizontal = property( _has_horizontal )

    def _has_vertical( self ):
        return bool( self.face_flags & FT_FACE_FLAG_VERTICAL )
    has_vertical = property( _has_vertical )

    def _has_kerning( self ):
        return bool( self.face_flags & FT_FACE_FLAG_KERNING )
    has_kerning = property( _has_kerning )

    def _is_scalable( self ):
        return bool( self.face_flags & FT_FACE_FLAG_SCALABLE )
    is_scalable = property( _is_scalable )

    def _is_sfnt( self ):
        return bool( self.face_flags & FT_FACE_FLAG_SFNT )
    is_sfnt = property( _is_sfnt )

    def _is_fixed_width( self ):
        return bool( self.face_flags & FT_FACE_FLAG_FIXED_WIDTH )
    is_fixed_width = property( _is_fixed_width )
    
    def _has_fixed_sizes( self ):
        return bool( self.face_flags & FT_FACE_FLAG_FIXED_SIZES )
    has_fixed_sizes = property( _has_fixed_sizes )

    def _has_glyph_names( self ):
        return bool( self.face_flags & FT_FACE_FLAG_GLYPH_NAMES )
    has_glyph_names = property( _has_glyph_names )

    def _has_multiple_masters( self ):
        return bool( self.face_flags & FT_FACE_FLAG_MULTIPLE_MASTERS )
    has_multiple_masters = property( _has_multiple_masters )

    def _is_cid_keyed( self ):
        return bool( self.face_flags & FT_FACE_FLAG_CID_KEYED )
    is_cid_keyed = property( _is_cid_keyed )

    def _is_tricky( self ):
        return bool( self.face_flags & FT_FACE_FLAG_TRICKY )
    is_tricky = property( _is_tricky )


    num_faces  = property(lambda self: self._FT_Face.contents.num_faces)
    face_index = property(lambda self: self._FT_Face.contents.face_index)

    face_flags = property(lambda self: self._FT_Face.contents.face_flags)
    style_flags = property(lambda self: self._FT_Face.contents.style_flags)

    num_glyphs = property(lambda self: self._FT_Face.contents.num_glyphs)

    family_name = property(lambda self: self._FT_Face.contents.family_name)
    style_name = property(lambda self: self._FT_Face.contents.style_name)

    num_fixed_sizes = property(lambda self: self._FT_Face.contents.num_fixed_sizes)
    def _get_available_sizes( self ):
        sizes = []
        n = self.num_fixed_sizes
        FT_sizes = self._FT_Face.contents.available_sizes
        for i in range(n):
            sizes.append( BitmapSize(FT_sizes[i]) )
        return sizes
    available_sizes = property(_get_available_sizes)

    num_charmaps = property(lambda self: self._FT_Face.contents.num_charmaps)
    def _get_charmaps( self ):
        charmaps = []
        n = self._FT_Face.contents.num_charmaps
        FT_charmaps = self._FT_Face.contents.charmaps
        for i in range(n):
            charmaps.append( Charmap(FT_charmaps[i]) )
        return charmaps
    charmaps = property(_get_charmaps)

    #       ('generic', FT_Generic),

    def _get_bbox( self ):
        return BBox( self._FT_Face.contents.bbox )
    bbox = property( _get_bbox )

    units_per_EM       = property(lambda self: self._FT_Face.contents.units_per_EM)
    ascender           = property(lambda self: self._FT_Face.contents.ascender)
    descender          = property(lambda self: self._FT_Face.contents.descender)
    height             = property(lambda self: self._FT_Face.contents.height)
    max_advance_width  = property(lambda self: self._FT_Face.contents.max_advance_width)
    max_advance_height = property(lambda self: self._FT_Face.contents.max_advance_height)
    underline_position = property(lambda self: self._FT_Face.contents.underline_position)
    underline_thickness= property(lambda self: self._FT_Face.contents.underline_thickness)

    def _get_glyph( self ):
        return GlyphSlot( self._FT_Face.contents.glyph )
    glyph = property( _get_glyph )

    def _get_size( self ):
        size = self._FT_Face.contents.size
        metrics = size.contents.metrics
        return SizeMetrics(metrics)
    size = property( _get_size)

    def _get_charmap( self ):
        return Charmap( self._FT_Face.contents.charmap)
    charmap = property( _get_charmap)



# -----------------------------------------------------------------------------
#  SfntName wrapper
# -----------------------------------------------------------------------------
class SfntName( object ):
    ''' '''
    def __init__(self, name):
        self._FT_SfntName = name

    platform_id  = property(lambda self: self._FT_SfntName.platform_id)
    encoding_id = property(lambda self: self._FT_SfntName.encoding_id)
    language_id = property(lambda self: self._FT_SfntName.language_id)
    name_id     = property(lambda self: self._FT_SfntName.name_id)
    #string      = property(lambda self: self._FT_SfntName.string)
    string_len  = property(lambda self: self._FT_SfntName.string_len)
    def _get_string(self):
    #     #s = self._FT_SfntName
         s = string_at(self._FT_SfntName.string, self._FT_SfntName.string_len)
         return s
    #     #return s.decode('utf-16be', 'ignore')
    #     return s.decode('utf-8', 'ignore')
    #     #n = s.string_len
    #     #data = [s.string[i] for i in range(n)]
    #     #return data
    string = property(_get_string)



# -----------------------------------------------------------------------------
#  FT_Stroker wrapper
# -----------------------------------------------------------------------------
class Stroker( object ):
    '''
    FT_Stroker wrapper

    This component generates stroked outlines of a given vectorial glyph. It
    also allows you to retrieve the 'outside' and/or the 'inside' borders of
    the stroke.

    This can be useful to generate 'bordered' glyph, i.e., glyphs displayed
    with a coloured (and anti-aliased) border around their shape.
    '''

    def __init__( self ):
        '''
        Create a new Stroker object.
        '''
        library = get_handle( )
        stroker = FT_Stroker( )
        error = FT_Stroker_New( library, byref(stroker) )
        if error: raise FT_Exception( error )
        self._FT_Stroker = stroker


    def __del__( self ):
        '''
        Destroy object.
        '''
        FT_Stroker_Done( self._FT_Stroker )


    def set( self, radius, line_cap, line_join, miter_limit ):
        '''
        Reset a stroker object's attributes.

        Parameters:
        -----------
          radius     : The border radius.
          line_cap   : The line cap style.
          line_join  : The line join style.
          miter_limit: The miter limit for the FT_STROKER_LINEJOIN_MITER
                       style, expressed as 16.16 fixed point value.

        Note:
        -----
          The radius is expressed in the same units as the outline
          coordinates.
        '''
        FT_Stroker_Set( self._FT_Stroker,
                        radius, line_cap, line_join, miter_limit )


    def rewind( self ):
        '''
        Reset a stroker object without changing its attributes. You should call
        this function before beginning a new series of calls to
        FT_Stroker_BeginSubPath or FT_Stroker_EndSubPath.
        '''
        FT_Stroker_Rewind( self._FT_Stroker )


    def parse_outline( self, outline, opened ):
        '''
        A convenience function used to parse a whole outline with the
        stroker. The resulting outline(s) can be retrieved later by functions
        like FT_Stroker_GetCounts and FT_Stroker_Export.

        Parameters:
        -----------
          outline: The source outline.
          opened : A boolean. If 1, the outline is treated as an open path
                   instead of a closed one.

        Note:
        -----
          If 'opened' is 0 (the default), the outline is treated as a closed
          path, and the stroker generates two distinct 'border' outlines.

          If 'opened' is 1, the outline is processed as an open path, and the
          stroker generates a single 'stroke' outline.

          This function calls 'rewind' automatically.
        '''
        error = FT_Stroker_ParseOutline( self._FT_Stroker, outline, opened)
        if error: raise FT_Exception( error )


    def begin_subpath( self, to, open_ ):
        '''
        Start a new sub-path in the stroker.

        Parameters:
        -----------
          to   : A pointer to the start vector.
          open_: A boolean. If 1, the sub-path is treated as an open one.

        Note:
        -----
          This function is useful when you need to stroke a path that is not
          stored as an 'Outline' object.
        '''
        error = FT_Stroker_BeginSubPath( self._FT_Stroker, to, open_ )
        if error: raise FT_Exception( error )

    
    def end_subpath( self ):
        '''
        Close the current sub-path in the stroker.

        Note:
        -----
          You should call this function after 'begin_subpath'. If the subpath
          was not 'opened', this function 'draws' a single line segment to the
          start position when needed.
        '''
        error = FT_Stroker_EndSubPath( self._FT_Stroker)
        if error: raise FT_Exception( error )

    
    def line_to( self, to ):
        '''
        'Draw' a single line segment in the stroker's current sub-path, from
        the last position.

        Parameters:
        -----------
          to: A pointer to the destination point.

        Note:
        -----
          You should call this function between 'begin_subpath' and
          'end_subpath'.
        '''
        error = FT_Stroker_LineTo( self._FT_Stroker, to )
        if error: raise FT_Exception( error )

        
    def conic_to( self, control, to ):
        '''
        'Draw' a single quadratic Bezier in the stroker's current sub-path,
        from the last position.

        Parameters:
        -----------
          control: A pointer to a Bezier control point.
          to     : A pointer to the destination point.

        Note:
        -----
          You should call this function between 'begin_subpath' and
          'end_subpath'.
        '''
        error = FT_Stroker_ConicTo( self._FT_Stroker, control, to )
        if error: raise FT_Exception( error )
        

    def cubic_to( self, control1, control2, to ):
        '''
        'Draw' a single quadratic Bezier in the stroker's current sub-path,
        from the last position.

        Parameters:
        -----------
          control1: A pointer to the first Bezier control point.
          control2: A pointer to second Bezier control point.
          to      : A pointer to the destination point.

        Note:
        -----
          You should call this function between 'begin_subpath' and
          'end_subpath'.
        '''
        error = FT_Stroker_CubicTo( self._FT_Stroker, control1, control2, to )
        if error: raise FT_Exception( error )
        
        
    def get_border_counts( self, border ):
        '''
        Call this function once you have finished parsing your paths with the
        stroker. It returns the number of points and contours necessary to
        export one of the 'border' or 'stroke' outlines generated by the
        stroker.
        
        Parameters:
        -----------
          border: The border index.

        Return:
        -------
          number of points, number of contours
        '''
        anum_points = FT_UInt()
        anum_contours = FT_UInt()
        error = FT_Stroker_GetBorderCounts( self._FT_Stroker, border,
                                    byref(anum_points), byref(anum_contours) )
        if error: raise FT_Exception( error )
        return anum_points.value, anum_contours.value
                                            

    def export_border( self , border, outline ):
        '''
        Call this function after 'get_border_counts' to export the
        corresponding border to your own 'Outline' structure.

        Note that this function appends the border points and contours to your
        outline, but does not try to resize its arrays.

        Parameters:
        -----------
          border:  The border index.
          outline: The target outline.
            
        Note:
        -----
          Always call this function after get_border_counts to get sure that
          there is enough room in your 'Outline' object to receive all new
          data.

          When an outline, or a sub-path, is 'closed', the stroker generates
          two independent 'border' outlines, named 'left' and 'right'

          When the outline, or a sub-path, is 'opened', the stroker merges the
          'border' outlines with caps. The 'left' border receives all points,
          while the 'right' border becomes empty.

          Use the function export instead if you want to retrieve all borders
          at once.
        '''
        FT_Stroker_ExportBorder( self._FT_Stroker, border, outline._FT_Outline )


    def get_counts( self ):
        '''
        Call this function once you have finished parsing your paths with the
        stroker. It returns the number of points and contours necessary to
        export all points/borders from the stroked outline/path.

        Return:
        -------
          number of points, number of contours
        '''
        anum_points = FT_UInt()
        anum_contours = FT_UInt()
        error = FT_Stroker_GetCounts( self._FT_Stroker,
                                      byref(anum_points), byref(anum_contours) )
        if error: raise FT_Exception( error )
        return anum_points.value, anum_contours.value


    def export( self, outline ):
        '''
        Call this function after get_border_counts to export all borders to
        your own 'Outline' structure.

        Note that this function appends the border points and contours to your
        outline, but does not try to resize its arrays.

        Parameters:
        -----------
        outline: The target outline.
        '''
        FT_Stroker_Export( self._FT_Stroker, outline._FT_Outline )
